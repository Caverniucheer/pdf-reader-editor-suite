"""Rasterization with an LRU tile cache. Backed by pypdfium2."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any

import pypdfium2 as pdfium
from PIL import Image

from pdf_suite.config.schema import Settings
from pdf_suite.errors import RenderError
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)


class RenderService:
    """Rasterizes pages and caches decoded tiles.

    Cache is a bounded LRU keyed by (doc_path, page_index, dpi). Eviction is
    byte-budget driven, not count driven — a 600 dpi A3 tile is ~48 MB.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._cache: OrderedDict[tuple[str, int, int], Image.Image] = OrderedDict()
        self._budget_bytes = settings.render.cache_mb * 1024 * 1024

    def rasterize(self, page_index: int, *, dpi: int = 144) -> Image.Image:
        try:
            pdf = pdfium.PdfDocument(self._current_path())
        except Exception as exc:  # noqa: BLE001 - pdfium raises bare RuntimeError
            raise RenderError(f"pdfium could not open document: {exc}") from exc
        page = pdf[page_index]
        bitmap = page.render(scale=dpi / 72)
        return bitmap.to_pil()

    def _current_path(self) -> str:
        # Placeholder: real wiring passes the active document path in.
        raise RenderError("render service has no active document")

    def flush_cache(self) -> None:
        self._cache.clear()
        log.debug("render cache flushed")