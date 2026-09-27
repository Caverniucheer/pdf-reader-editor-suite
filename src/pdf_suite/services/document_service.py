"""Owns open documents. Enforces single-writer per path."""

from __future__ import annotations

from pathlib import Path

from pdf_suite.config.schema import Settings
from pdf_suite.core.document import PdfDocument
from pdf_suite.errors import EditError
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)


class DocumentService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._open: dict[Path, PdfDocument] = {}

    def open(self, path: Path, *, password: str | None = None) -> PdfDocument:
        key = path.resolve()
        if key in self._open:
            log.debug("reusing open handle for %s", key)
            return self._open[key]
        doc = PdfDocument(key, password=password)
        self._open[key] = doc
        return doc

    def acquire_write(self, path: Path) -> None:
        """Raise if another writer holds the path. Single-writer invariant."""
        key = path.resolve()
        if key in self._open and getattr(self._open[key], "_dirty", False):
            raise EditError(f"document already open for edit: {key}", path=str(key))

    def close_all(self) -> None:
        for doc in self._open.values():
            doc.close()
        self._open.clear()