"""Sarvam Bulbul v3 TTS adapter."""
import base64
import logging
import time

import httpx

from app.config import get_settings
from app.models.schema import Language, SpeechResponse

logger = logging.getLogger(__name__)

API_BASE = "https://api.sarvam.ai"
TTS_EP = f"{API_BASE}/v1/tts"
MODEL = "bulbul:v3"
LANG_CODES = {Language.MARATHI: "mr-IN", Language.HINDI: "hi-IN", Language.ENGLISH: "en-IN"}
DEFAULT_SPEAKERS = {Language.MARATHI: "anushka", Language.HINDI: "anushka", Language.ENGLISH: "madhav"}
MAX_RETRIES = 2


class SarvamTTSError(Exception):
    pass


class SarvamTTSProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or get_settings().sarvam_api_key

    def speak(
        self,
        text: str,
        language: Language = Language.MARATHI,
        speaker: str | None = None,
        output_format: str = "mp3",
    ) -> SpeechResponse:
        if not self.api_key:
            raise SarvamTTSError("SARVAM_API_KEY not configured")
        payload = {
            "model": MODEL,
            "input": text,
            "language": LANG_CODES.get(language, "mr-IN"),
            "speaker": speaker or DEFAULT_SPEAKERS.get(language, "anushka"),
            "speechSampleRate": 24000,
        }
        headers = {"Content-Type": "application/json", "api-subscription-key": self.api_key}
        for attempt in range(MAX_RETRIES):
            try:
                with httpx.Client(timeout=30) as c:
                    r = c.post(TTS_EP, headers=headers, json=payload)
                if r.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                r.raise_for_status()
                data = r.json()
                audio = base64.b64decode(data.get("audio", ""))
                return SpeechResponse(audio=audio, format=output_format)
            except httpx.TimeoutException:
                if attempt < MAX_RETRIES - 1:
                    continue
                raise SarvamTTSError("TTS timed out")
        raise SarvamTTSError("Max retries exceeded")
