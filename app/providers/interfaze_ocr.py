"""Interfaze OCR adapter (OpenAI-compatible SDK).

NOTE: Verify the exact response shape at https://interfaze.ai/docs
before relying on the parsing below.
"""
import base64
import logging
import time

from app.config import get_settings
from app.models.schema import OCRPage, OCRResult, OCRWord

logger = logging.getLogger(__name__)

BASE_URL = "https://api.interfaze.ai/v1"
MODEL = "interfaze-beta"
TIMEOUT = 30
MAX_RETRIES = 3


class InterfazeOCRError(Exception):
    pass


class InterfazeOCRProvider:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or get_settings().interfaze_api_key
        if not self.api_key:
            logger.warning("INTERFAZE_API_KEY not set – provider will fail.")

    def read(self, image_bytes: bytes) -> OCRResult:
        import openai

        client = openai.OpenAI(base_url=BASE_URL, api_key=self.api_key, timeout=TIMEOUT)
        b64 = base64.b64encode(image_bytes).decode()
        data_url = f"data:image/png;base64,{b64}"

        for attempt in range(MAX_RETRIES):
            try:
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "<task>ocr</task>"},
                        {
                            "role": "user",
                            "content": [
                                {"type": "image_url", "image_url": {"url": data_url}},
                            ],
                        },
                    ],
                )
                raw = resp.choices[0].message.content or ""
                return self._parse(raw)
            except Exception as exc:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise InterfazeOCRError(f"Interfaze OCR failed: {exc}") from exc
        raise InterfazeOCRError("Max retries exceeded")

    @staticmethod
    def _parse(raw: str) -> OCRResult:
        """Normalise Interfaze response into OCRResult.

        TODO: adjust once the exact response schema is confirmed.
        """
        import json

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return OCRResult(
                pages=[OCRPage(page_number=1, full_text=raw, avg_confidence=0.5)],
                full_text=raw,
            )

        words = []
        for w in data.get("words", []):
            words.append(
                OCRWord(
                    text=w.get("text", ""),
                    conf=float(w.get("confidence", 0.0)),
                    bbox=w.get("bbox"),
                )
            )
        full = data.get("full_text", " ".join(w.text for w in words))
        return OCRResult(
            pages=[OCRPage(page_number=1, words=words, full_text=full, avg_confidence=0.8)],
            full_text=full,
        )
