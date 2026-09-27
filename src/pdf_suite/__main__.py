"""Entry point for `python -m pdf_suite` and the `pdf-suite` console script."""

from __future__ import annotations

import sys

from pdf_suite.app.bootstrap import bootstrap
from pdf_suite.config.loader import load_settings
from pdf_suite.utils.logging import configure_logging


def main(argv: list[str] | None = None) -> int:
    """Boot the desktop shell. Returns process exit code."""
    args = list(sys.argv[1:] if argv is None else argv)
    settings = load_settings()
    configure_logging(settings.log_level, settings.log_dir)
    return bootstrap(args, settings)


if __name__ == "__main__":
    raise SystemExit(main())