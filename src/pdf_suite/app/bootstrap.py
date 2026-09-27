"""Compose services, register handlers, launch the desktop shell."""

from __future__ import annotations

from pdf_suite.app.lifecycle import Lifecycle
from pdf_suite.config.schema import Settings
from pdf_suite.services.document_service import DocumentService
from pdf_suite.services.render_service import RenderService
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)


def bootstrap(argv: list[str], settings: Settings) -> int:
    """Wire the app and hand off to the shell. Returns exit code."""
    docs = DocumentService(settings)
    render = RenderService(settings)
    lifecycle = Lifecycle(docs=docs, render=render, settings=settings)
    lifecycle.on_start()
    try:
        return lifecycle.run(argv)
    finally:
        lifecycle.on_stop()