"""Sarvam AI LLM adapter (explain-only, never decides)."""
import logging
import time

import httpx

from app.config import get_settings
from app.models.schema import ExplanationResponse, Language

logger = logging.getLogger(__name__)

API_BASE = "https://api.sarvam.ai"
CHAT_EP = f"{API_BASE}/v1/chat/completions"
DEFAULT_MODEL = "sarvam-m"
MAX_RETRIES = 3

DISCLAIMERS = {
    Language.ENGLISH: (
        "This analysis is for informational purposes only and does not constitute "
        "legal advice. Please consult a qualified advocate."
    ),
    Language.MARATHI: (
        "हे विश्लेषण केवळ माहितीसाठी आहे आणि कायदेशीर सल्ला नाही. "
        "कृपया योग्य वकीलाशी संपर्क साधा."
    ),
    Language.HINDI: (
        "यह विश्लेषण केवल सूचना के लिए है और कानूनी सलाह नहीं है। "
        "कृपया योग्य वकील से संपर्क करें।"
    ),
}


class SarvamLLMError(Exception):
    pass


class SarvamLLMProvider:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        s = get_settings()
        self.api_key = api_key or s.sarvam_api_key
        self.model = model or DEFAULT_MODEL

    def explain(
        self,
        payload: dict,
        language: Language = Language.ENGLISH,
        purpose: str = "general",
    ) -> ExplanationResponse:
        if not self.api_key:
            raise SarvamLLMError("SARVAM_API_KEY not configured")

        import json
        messages = [
            {"role": "system", "content": self._system(language, purpose)},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False, default=str)},
        ]
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 2000,
        }
        headers = {"Content-Type": "application/json", "api-subscription-key": self.api_key}

        for attempt in range(MAX_RETRIES):
            try:
                with httpx.Client(timeout=60) as c:
                    r = c.post(CHAT_EP, headers=headers, json=body)
                if r.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                if r.status_code == 401:
                    raise SarvamLLMError("Auth failed – check SARVAM_API_KEY")
                r.raise_for_status()
                data = r.json()
                text = data["choices"][0]["message"]["content"]
                return ExplanationResponse(
                    summary=text,
                    disclaimer=DISCLAIMERS.get(language, DISCLAIMERS[Language.ENGLISH]),
                    model_used=self.model,
                    tokens_used=data.get("usage", {}).get("total_tokens"),
                )
            except httpx.TimeoutException:
                if attempt < MAX_RETRIES - 1:
                    continue
                raise SarvamLLMError("Sarvam request timed out")
        raise SarvamLLMError("Max retries exceeded")

    @staticmethod
    def _system(lang: Language, purpose: str) -> str:
        lang_name = {"en": "English", "mr": "Marathi", "hi": "Hindi"}.get(lang.value, "English")
        return (
            f"You explain a Maharashtra land record to an ordinary person.\n"
            f"Write in {lang_name}. Short sentences. School-level reading level.\n"
            f"Use ONLY facts in the input JSON. Never invent. Never say safe/clean/valid.\n"
            f"If a field is missing say 'not shown on this document'.\n"
            f"Structure: What this document says / Things to be careful about / What to do next.\n"
            f"End with: informational only, not legal advice.\n"
            f"Purpose: {purpose}."
        )
