"""Export a page range to PNG or plain text."""

from __future__ import annotations

from pathlib import Path

from pdf_suite.errors import RenderError
from pdf_suite.services.render_service import RenderService


class ExportHandler:
    def __init__(self, render: RenderService) -> None:
        self._render = render

    def export_png(self, page_index: int, out: Path, *, dpi: int = 144) -> Path:
        if dpi < 36 or dpi > 600:
            raise RenderError(f"dpi out of range: {dpi}")
        image = self._render.rasterize(page_index, dpi=dpi)
        out.parent.mkdir(parents=True, exist_ok=True)
        image.save(out, format="PNG", optimize=True)
        return out