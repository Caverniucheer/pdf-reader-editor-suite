"""Smoke tests for the document layer. Uses a generated minimal PDF."""

from __future__ import annotations

from pathlib import Path

import pikepdf
import pytest

from pdf_suite.core.document import PdfDocument
from pdf_suite.errors import ParseError


@pytest.fixture()
def blank_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "blank.pdf"
    with pikepdf.Pdf.new() as pdf:
        pdf.add_blank_page(page_size=(612, 792))
        pdf.save(path)
    return path


def test_page_count(blank_pdf: Path) -> None:
    doc = PdfDocument(blank_pdf)
    try:
        assert doc.page_count == 1
    finally:
        doc.close()


def test_media_box_roundtrip(blank_pdf: Path) -> None:
    doc = PdfDocument(blank_pdf)
    try:
        page = next(doc.pages())
        assert page.width_pt == pytest.approx(612.0)
        assert page.height_pt == pytest.approx(792.0)
    finally:
        doc.close()


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ParseError):
        PdfDocument(tmp_path / "nope.pdf")