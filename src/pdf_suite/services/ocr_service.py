"""Optional OCR pipeline. Only loaded when the `ocr` extra is installed."""

from __future__ import annotations

from pathlib import Path

from pdf_suite.errors import PdfSuiteError
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)


class OcrService:
    def __init__(self, *, lang: str = "eng") -> None:
        self._lang = lang
        self._available = self._probe()

    def _probe(self) -> bool:
        try:
            import pytesseract  # noqa: F401
        except ImportError:
            log.info("pytesseract not installed; OCR disabled")
            return False
        return True

    def extract_text(self, image_path: Path) -> str:
        if not self._available:
            raise PdfSuiteError("OCR extra not installed")
        import pytesseract

        return pytesseract.image_to_string(str(image_path), lang=self._lang)