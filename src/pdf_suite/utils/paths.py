"""Path normalization and safety checks for user-supplied paths."""

from __future__ import annotations

from pathlib import Path

from pdf_suite.errors import PdfSuiteError

_ALLOWED_SUFFIXES = {".pdf"}


def normalize_pdf_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if resolved.suffix.lower() not in _ALLOWED_SUFFIXES:
        raise PdfSuiteError(f"not a PDF: {resolved}", path=str(resolved))
    if not resolved.exists():
        raise PdfSuiteError(f"file not found: {resolved}", path=str(resolved))
    return resolved


def ensure_within(base: Path, candidate: Path) -> Path:
    """Reject any path that escapes `base` after NTFS normalization."""
    base_r = base.resolve()
    cand_r = candidate.resolve()
    if base_r not in cand_r.parents and cand_r != base_r:
        raise PdfSuiteError(f"path escapes sandbox: {cand_r}", path=str(cand_r))
    return cand_r