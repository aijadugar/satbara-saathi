"""Abstract interfaces – every external model call sits behind these."""
from typing import Protocol, runtime_checkable

from app.models.schema import (
    ExplanationResponse,
    Language,
    OCRResult,
    SpeechResponse,
)


@runtime_checkable
class OCRProvider(Protocol):
    def read(self, image_bytes: bytes) -> OCRResult: ...


@runtime_checkable
class LLMProvider(Protocol):
    def explain(
        self,
        payload: dict,
        language: Language = Language.ENGLISH,
        purpose: str = "general",
    ) -> ExplanationResponse: ...


@runtime_checkable
class SpeechProvider(Protocol):
    def speak(
        self,
        text: str,
        language: Language = Language.MARATHI,
        speaker: str | None = None,
        output_format: str = "mp3",
    ) -> SpeechResponse: ...
