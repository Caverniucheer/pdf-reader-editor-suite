"""Thin shell wrapper. Qt is optional; falls back to CLI when headless."""

from __future__ import annotations

from dataclasses import dataclass

from pdf_suite.services.document_service import DocumentService
from pdf_suite.services.render_service import RenderService
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class Shell:
    docs: DocumentService
    render: RenderService

    def exec_(self, argv: list[str]) -> int:
        try:
            from pdf_suite.ui.main_window import MainWindow  # type: ignore[import-not-found]
        except ImportError:
            log.warning("Qt shell unavailable; running headless CLI")
            from pdf_suite.cli.app import run

            return run(argv)
        return MainWindow(docs=self.docs, render=self.render).run(argv)