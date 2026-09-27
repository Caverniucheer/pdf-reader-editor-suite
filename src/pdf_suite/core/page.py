"""Page proxy. Lazily materializes geometry and content streams."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pdf_suite.core.document import PdfDocument


@dataclass(slots=True)
class Page:
    doc: "PdfDocument"
    index: int
    _media_box: tuple[float, float, float, float] | None = field(default=None, repr=False)

    @property
    def media_box(self) -> tuple[float, float, float, float]:
        """(x0, y0, x1, y1) in PDF user units (1/72 inch)."""
        if self._media_box is None:
            raw = self.doc._pdf.pages[self.index].MediaBox  # noqa: SLF001
            self._media_box = tuple(float(v) for v in raw)  # type: ignore[assignment]
        return self._media_box

    @property
    def width_pt(self) -> float:
        x0, _, x1, _ = self.media_box
        return x1 - x0

    @property
    def height_pt(self) -> float:
        _, y0, _, y1 = self.media_box
        return y1 - y0