"""Shared error hierarchy. Every raised error in the suite derives here."""

from __future__ import annotations


class PdfSuiteError(Exception):
    """Base class for all pdf_suite errors."""

    code: str = "PDF_SUITE_ERROR"

    def __init__(self, message: str, *, path: str | None = None) -> None:
        super().__init__(message)
        self.path = path

    def as_dict(self) -> dict[str, str | None]:
        return {"code": self.code, "message": str(self), "path": self.path}


class ParseError(PdfSuiteError):
    code = "PARSE_ERROR"


class RenderError(PdfSuiteError):
    code = "RENDER_ERROR"


class EditError(PdfSuiteError):
    code = "EDIT_ERROR"


class SandboxViolation(PdfSuiteError):
    code = "SANDBOX_VIOLATION"


class NativeModuleUnavailable(PdfSuiteError):
    code = "NATIVE_UNAVAILABLE"