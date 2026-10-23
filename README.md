# Satbara Saathi (सातबारा साथी)

Understand Maharashtra 7/12 (Satbara) extracts in plain **Marathi / Hindi / English**.

## What it does
1. Reads a 7/12 image (scanned or digital)
2. Extracts structured data via OCR
3. Runs deterministic red-flag rules (no AI in the rules engine)
4. Explains findings in plain language via LLM
5. Speaks the summary aloud (TTS)

## What it does NOT do
- Give legal advice
- Decide if land is "safe"
- Store your images or personal data
- Process 8A, mutation extracts, or other states (yet)

## Quick start
```bash
cp .env.example .env
pip install -e ".[dev]"
make dev        # http://localhost:8000
make test       # run tests with fake providers
```

## Architecture
```
Upload → Preprocess → OCR → Extract → Validate → Rules → Explain → TTS
                                         ↕
                                   Confirm fields
```

## Privacy
- Images deleted after processing
- No PII in logs
- Anonymous impact counters only
- Consent gate before upload

## License
Apache-2.0
