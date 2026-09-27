"""Structured logging. Single configure call, idempotent."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_CONFIGURED = False
_FORMAT = "%(asctime)s %(levelname)-7s %(name)s :: %(message)s"


def configure_logging(level: str, log_dir: Path) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    log_dir.mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(log_dir / "pdf_suite.log", encoding="utf-8"),
    ]
    logging.basicConfig(level=level.upper(), format=_FORMAT, handlers=handlers)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)