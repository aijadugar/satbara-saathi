from app.models.schema import Language
from app.pipeline.speak import chunk_text, speak
from app.providers.fake_providers import FakeTTSProvider


def test_chunk_short():
    assert chunk_text("hello") == ["hello"]


def test_chunk_long():
    text = "वाक्य. " * 500
    chunks = chunk_text(text, max_chars=100)
    assert all(len(c) <= 100 for c in chunks)


def test_speak_fake():
    p = FakeTTSProvider()
    r = speak(p, "नमस्कार", Language.MARATHI)
    assert len(r.audio) > 0
