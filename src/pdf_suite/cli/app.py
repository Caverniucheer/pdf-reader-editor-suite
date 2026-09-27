"""Typer CLI for headless render, extract, and inspect operations."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from pdf_suite.config.loader import load_settings
from pdf_suite.handlers.open_handler import OpenHandler
from pdf_suite.services.document_service import DocumentService

app = typer.Typer(help="pdf-reader-editor-suite CLI", no_args_is_help=True)
console = Console()


@app.command()
def info(path: Path) -> None:
    """Print page count and media box of the first page."""
    settings = load_settings()
    docs = DocumentService(settings)
    doc = OpenHandler(docs).handle(str(path))
    first = next(doc.pages())
    w, h = first.width_pt, first.height_pt
    console.print(f"{path.name}: {doc.page_count} pages, first={w:.1f}x{h:.1f} pt")


def run(argv: list[str] | None = None) -> int:
    try:
        app(args=argv, standalone_mode=False)
    except typer.Exit as exc:
        return int(exc.exit_code or 0)
    return 0