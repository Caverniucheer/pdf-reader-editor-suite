"""Locate, merge, and persist settings. User file overrides packaged defaults."""

from __future__ import annotations

import json
import os
from pathlib import Path

from pdf_suite.config.schema import Settings
from pdf_suite.errors import PdfSuiteError

APP_DIRNAME = "pdf-reader-editor-suite"


def _user_config_path() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home())
    return Path(base) / APP_DIRNAME / "settings.json"


def load_settings() -> Settings:
    """Load settings, merging user overrides over defaults."""
    path = _user_config_path()
    if not path.exists():
        return Settings()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PdfSuiteError(f"failed to read settings: {exc}", path=str(path)) from exc
    return Settings.model_validate(raw)


def save_settings(settings: Settings) -> Path:
    """Persist settings to the per-user config path. Returns the path written."""
    path = _user_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(settings.model_dump_json(indent=2), encoding="utf-8")
    return path