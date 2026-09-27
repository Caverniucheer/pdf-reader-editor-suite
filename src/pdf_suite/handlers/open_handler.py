"""Handle open-document requests from UI and CLI."""

from __future__ import annotations

from pathlib import Path

from pdf_suite.core.document import PdfDocument
from pdf_suite.errors import PdfSuiteError
from pdf_suite.services.document_service import DocumentService
from pdf_suite.utils.paths import normalize_pdf_path


class OpenHandler:
    def __init__(self, docs: DocumentService) -> None:
        self._docs = docs

    def handle(self, raw_path: str, *, password: str | None = None) -> PdfDocument:
        path = normalize_pdf_path(Path(raw_path))
        try:
            return self._docs.open(path, password=password)
        except PdfSuiteError:
            raise
        except OSError as exc:
            raise PdfSuiteError(f"cannot open {path}: {exc}", path=str(path)) from exc