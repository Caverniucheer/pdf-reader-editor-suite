"""Lifecycle owner. Owns service shutdown order and crash-safe teardown."""

from __future__ import annotations

from dataclasses import dataclass

from pdf_suite.config.schema import Settings
from pdf_suite.services.document_service import DocumentService
from pdf_suite.services.render_service import RenderService
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class Lifecycle:
    docs: DocumentService
    render: RenderService
    settings: Settings

    def on_start(self) -> None:
        self.settings.cache_dir.mkdir(parents=True, exist_ok=True)
        log.info("pdf-suite started; cache_dir=%s", self.settings.cache_dir)

    def run(self, argv: list[str]) -> int:
        # Shell is imported lazily so headless CLI paths skip Qt.
        from pdf_suite.app.shell import Shell

        return Shell(docs=self.docs, render=self.render).exec_(argv)

    def on_stop(self) -> None:
        self.render.flush_cache()
        self.docs.close_all()
        log.info("pdf-suite stopped cleanly")