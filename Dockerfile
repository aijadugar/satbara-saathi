FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# System libraries commonly needed by OCR / image-processing packages.
# Remove or add packages to match what your project actually uses.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# If you use Tesseract for OCR, add these to the list above:
#   tesseract-ocr tesseract-ocr-mar tesseract-ocr-hin tesseract-ocr-eng poppler-utils

# Copy the whole project (see .dockerignore for what is excluded)
COPY . .

# Install the app (no [dev] extras in production)
RUN pip install -e .

# Run as a non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Render injects $PORT at runtime. Locally it defaults to 8000.
# IMPORTANT: replace "app.main:app" with the module path your Makefile's `dev` target uses.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
