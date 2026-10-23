"""Image preprocessing: EXIF fix, deskew, denoise, contrast, quality check."""
import io
import logging

import cv2
import numpy as np
from PIL import Image, ImageOps
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
BLUR_THRESHOLD = 50.0
MIN_QUALITY = 0.4


class PreprocessingError(Exception):
    pass


class QualityScore(BaseModel):
    blur_score: float = Field(ge=0.0, le=1.0)
    brightness_score: float = Field(ge=0.0, le=1.0)
    overall_score: float = Field(ge=0.0, le=1.0)
    is_acceptable: bool = False
    warnings: list[str] = Field(default_factory=list)


def preprocess_image(image_bytes: bytes) -> tuple[bytes, QualityScore]:
    if len(image_bytes) > MAX_FILE_SIZE:
        raise PreprocessingError("File exceeds 10 MB limit")
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
    except Exception as exc:
        raise PreprocessingError(f"Cannot read image: {exc}") from exc

    arr = np.array(img)

    # deskew
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    if lines is not None and len(lines):
        angles = [np.arctan2(l[0][3] - l[0][1], l[0][2] - l[0][0]) * 180 / np.pi for l in lines]
        med = float(np.median(angles))
        if abs(med) > 0.5:
            h, w = arr.shape[:2]
            M = cv2.getRotationMatrix2D((w // 2, h // 2), med, 1.0)
            arr = cv2.warpAffine(arr, M, (w, h), borderValue=(255, 255, 255))

    # denoise + contrast
    arr = cv2.fastNlMeansDenoisingColored(arr, None, 10, 10, 7, 21)
    lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    arr = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2RGB)

    # quality
    gray2 = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    blur_var = cv2.Laplacian(gray2, cv2.CV_64F).var()
    blur_score = min(blur_var / 200.0, 1.0)
    brightness = gray2.mean() / 255.0
    bright_score = 1.0 if 0.2 <= brightness <= 0.9 else max(0.0, 1.0 - abs(brightness - 0.55))
    overall = blur_score * 0.6 + bright_score * 0.4
    warnings: list[str] = []
    if blur_score < 0.5:
        warnings.append("Image appears blurry – please retake.")
    if bright_score < 0.5:
        warnings.append("Lighting is poor – please retake with better light.")

    out = Image.fromarray(arr)
    buf = io.BytesIO()
    out.save(buf, format="PNG")
    return buf.getvalue(), QualityScore(
        blur_score=blur_score,
        brightness_score=bright_score,
        overall_score=overall,
        is_acceptable=overall >= MIN_QUALITY,
        warnings=warnings,
    )
