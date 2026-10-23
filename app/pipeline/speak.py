"""TTS pipeline: chunk → synthesise → concatenate → cache."""
import hashlib
import logging
import re
import tempfile
from pathlib import Path

from app.models.schema import Language, SpeechResponse
from app.providers.base import SpeechProvider

logger = logging.getLogger(__name__)

CACHE_DIR = Path(tempfile.gettempdir()) / "satbara_tts_cache"
MAX_CHUNK = 2000


def chunk_text(text: str, max_chars: int = MAX_CHUNK) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    sentences = re.split(r"[.!?।]+", text)
    chunks: list[str] = []
    cur = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(f"{cur} {s}".strip()) <= max_chars:
            cur = f"{cur} {s}".strip()
        else:
            if cur:
                chunks.append(cur)
            cur = s
    if cur:
        chunks.append(cur)
    return chunks


def get_cache_key(text: str, lang: Language, fmt: str) -> str:
    return hashlib.sha256(f"{text}:{lang.value}:{fmt}".encode()).hexdigest()[:32]


def speak(
    provider: SpeechProvider,
    text: str,
    language: Language = Language.MARATHI,
    output_format: str = "mp3",
) -> SpeechResponse:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    key = get_cache_key(text, language, output_format)
    cached = CACHE_DIR / f"{key}.{output_format}"
    if cached.exists():
        return SpeechResponse(audio=cached.read_bytes(), format=output_format)

    chunks = chunk_text(text)
    parts: list[bytes] = []
    for c in chunks:
        resp = provider.speak(c, language=language, output_format=output_format)
        parts.append(resp.audio)

    audio = b"".join(parts) if output_format == "mp3" else parts[0]
    try:
        cached.write_bytes(audio)
    except OSError:
        pass
    return SpeechResponse(audio=audio, format=output_format)
