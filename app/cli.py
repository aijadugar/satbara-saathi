"""CLI: python -m app.cli ocr sample.jpg"""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "ocr":
        print("Usage: python -m app.cli ocr <image>")
        sys.exit(1)
    path = Path(sys.argv[2])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    from app.providers.fake_providers import FakeOCRProvider
    provider = FakeOCRProvider()
    result = provider.read(path.read_bytes())
    print(result.full_text)
    for page in result.pages:
        for w in page.words:
            if w.conf < 0.85:
                print(f"  LOW CONF: '{w.text}' ({w.conf:.2f})")


if __name__ == "__main__":
    main()
