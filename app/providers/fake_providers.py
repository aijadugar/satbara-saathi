"""Fake providers so the whole pipeline runs offline / in tests."""
import struct

from app.models.schema import (
    ExplanationResponse,
    Language,
    OCRPage,
    OCRResult,
    OCRWord,
    SpeechResponse,
)


class FakeOCRProvider:
    def __init__(self) -> None:
        self.call_count = 0

    def read(self, image_bytes: bytes) -> OCRResult:
        self.call_count += 1
        return OCRResult(
            pages=[
                OCRPage(
                    page_number=1,
                    words=[
                        OCRWord(text="गाव", conf=0.95),
                        OCRWord(text="पुणे", conf=0.98),
                        OCRWord(text="तालुका", conf=0.95),
                        OCRWord(text="हवेली", conf=0.97),
                        OCRWord(text="सर्वे", conf=0.90),
                        OCRWord(text="37", conf=0.99),
                    ],
                    full_text="गाव पुणे तालुका हवेली सर्वे 37",
                    avg_confidence=0.95,
                )
            ],
            full_text="गाव पुणे तालुका हवेली सर्वे 37",
        )


class FakeLLMProvider:
    def __init__(self) -> None:
        self.call_count = 0
        self.last_payload: dict = {}

    def explain(
        self,
        payload: dict,
        language: Language = Language.ENGLISH,
        purpose: str = "general",
    ) -> ExplanationResponse:
        self.call_count += 1
        self.last_payload = payload
        flags = payload.get("rules_result", {}).get("flags", [])
        serious = [f for f in flags if f.get("severity") == "serious"]
        if serious:
            summary = f"This document has {len(serious)} serious issue(s)."
        else:
            summary = "This document appears to be in order."
        return ExplanationResponse(
            summary=summary,
            field_explanations={},
            flag_explanations={f.get("rule_id", "?"): f.get("title_en", "") for f in flags},
            disclaimer="Informational only. Not legal advice.",
            model_used="fake-llm",
            tokens_used=0,
        )


class FakeTTSProvider:
    def __init__(self) -> None:
        self.call_count = 0

    def speak(
        self,
        text: str,
        language: Language = Language.MARATHI,
        speaker: str | None = None,
        output_format: str = "mp3",
    ) -> SpeechResponse:
        self.call_count += 1
        if output_format == "wav":
            audio = self._silent_wav(0.2)
        else:
            audio = b"\xff\xfb\x90\x00" + b"\x00" * 32
        return SpeechResponse(audio=audio, format=output_format, duration_seconds=0.2)

    @staticmethod
    def _silent_wav(dur: float) -> bytes:
        sr, ch, bits = 24000, 1, 16
        n = int(sr * dur)
        data = b"\x00\x00" * n
        hdr = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF", 36 + len(data), b"WAVE", b"fmt ", 16, 1, ch, sr,
            sr * ch * bits // 8, ch * bits // 8, bits, b"data", len(data),
        )
        return hdr + data
