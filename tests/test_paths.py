"""Unit tests for path normalization and sandbox containment."""

from __future__ import annotations

from pathlib import Path

import pytest

from pdf_suite.errors import PdfSuiteError
from pdf_suite.utils.paths import ensure_within, normalize_pdf_path


def test_reject_non_pdf(tmp_path: Path) -> None:
    bad = tmp_path / "notes.txt"
    bad.write_text("hi", encoding="utf-8")
    with pytest.raises(PdfSuiteError):
        normalize_pdf_path(bad)


def test_accept_pdf(tmp_path: Path) -> None:
    ok = tmp_path / "doc.PDF"
    ok.write_bytes(b"%PDF-1.7\n")
    assert normalize_pdf_path(ok) == ok.resolve()


def test_sandbox_escape(tmp_path: Path) -> None:
    base = tmp_path / "sandbox"
    base.mkdir()
    outside = tmp_path / "escape.txt"
    with pytest.raises(PdfSuiteError):
        ensure_within(base, outside)


def test_sandbox_inside(tmp_path: Path) -> None:
    base = tmp_path / "sandbox"
    base.mkdir()
    inside = base / "ok.txt"
    inside.write_text("x", encoding="utf-8")
    assert ensure_within(base, inside) == inside.resolve()