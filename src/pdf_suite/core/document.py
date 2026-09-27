"""Backing document handle wrapping pikepdf. Read-mostly, guard-heavy."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pikepdf

from pdf_suite.core.page import Page
from pdf_suite.errors import ParseError
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)


class PdfDocument:
    """Owns a pikepdf.Pdf handle and exposes a page iterator.

    Side effects: opens the file handle and, on non-encrypted docs, loads
    the full cross-reference table into memory. Encrypted docs stay lazy
    until `unlock()` is called.
    """

    def __init__(self, path: Path, *, password: str | None = None) -> None:
        self.path = path
        try:
            self._pdf = pikepdf.open(str(path), password=password or "")
        except pikepdf.PasswordError as exc:
            raise ParseError("document is encrypted; password required", path=str(path)) from exc
        except pikepdf.PdfError as exc:
            raise ParseError(f"failed to open: {exc}", path=str(path)) from exc
        self._pages: list[Page] | None = None

    @property
    def page_count(self) -> int:
        return len(self._pdf.pages)

    def pages(self) -> Iterator[Page]:
        if self._pages is None:
            self._pages = [Page(self, i) for i in range(self.page_count)]
        yield from self._pages

    def close(self) -> None:
        try:
            self._pdf.close()
        except Exception:  # noqa: BLE001 - teardown must never raise
            log.exception("error closing %s", self.path)