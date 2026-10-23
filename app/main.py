"""FastAPI application entry-point."""
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.config import get_settings
from app.models.schema import (
    HealthResponse, Language, ProcessingResult, ProcessingStatus,
)
from app.pipeline.preprocess import PreprocessingError, preprocess_image
from app.pipeline.extract import extract_from_structured
from app.pipeline.validate import validate
from app.pipeline.rules import RulesEngine
from app.pipeline.explain import generate_explanation
from app.pipeline.checklist import generate_checklist
from app.providers.fake_providers import FakeLLMProvider, FakeOCRProvider, FakeTTSProvider
from app.logging_.impact import ImpactDB

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)

# wire providers (swap via env vars in production)
ocr_provider = FakeOCRProvider()
llm_provider = FakeLLMProvider()
tts_provider = FakeTTSProvider()
rules_engine = RulesEngine()
impact_db = ImpactDB()

# in-memory job store (ephemeral – privacy by design)
jobs: dict[str, ProcessingResult] = {}

WEB_DIR = Path(__file__).parent.parent / "web"
if WEB_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR), html=True), name="web")


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        version=__version__,
        providers={"ocr": settings.provider_ocr, "llm": settings.provider_llm, "tts": settings.provider_tts},
        privacy_mode=not settings.log_personal_data,
    )


@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    language: str = Form("en"),
    purpose: str = Form("general"),
    consent: bool = Form(False),
    partner: str | None = Form(None),
    seller_name: str | None = Form(None),
):
    if not consent:
        raise HTTPException(400, "Consent is required before processing.")

    image = await file.read()
    try:
        image, quality = preprocess_image(image)
    except PreprocessingError as exc:
        raise HTTPException(422, str(exc))

    if not quality.is_acceptable:
        raise HTTPException(422, f"Image quality too low. {'; '.join(quality.warnings)}")

    ocr = ocr_provider.read(image)
    doc = extract_from_structured({}, ocr)  # placeholder until real structured extraction
    errors = validate(doc)

    rules_result = rules_engine.evaluate(doc, seller_name=seller_name)

    lang = Language(language) if language in ("en", "mr", "hi") else Language.ENGLISH
    explanation = generate_explanation(llm_provider, doc, rules_result, lang, purpose)
    checklist = generate_checklist(rules_result, purpose, lang)

    job_id = uuid.uuid4().hex[:12]
    jobs[job_id] = ProcessingResult(
        job_id=job_id,
        status=ProcessingStatus.COMPLETED,
        extract=doc,
        rules_result=rules_result,
        explanation=explanation,
    )

    impact_db.log_document(partner=partner, language=language)
    impact_db.log_flags([f.model_dump() for f in rules_result.flags], partner=partner)

    return {
        "job_id": job_id,
        "quality": quality.model_dump(),
        "validation_errors": errors,
        "flags": [f.model_dump() for f in rules_result.flags],
        "explanation": explanation.model_dump(),
        "checklist": checklist,
        "disclaimer": jobs[job_id].disclaimer,
    }


@app.get("/api/stats")
def stats(days: int = 30, partner: str | None = None):
    return impact_db.get_stats(days=days, partner=partner)
