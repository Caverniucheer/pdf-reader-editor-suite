"""Pydantic settings schema for the desktop app and CLI."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class RenderSettings(BaseModel):
    dpi: int = Field(default=144, ge=36, le=600)
    cache_mb: int = Field(default=512, ge=64, le=4096)
    tile_size: int = Field(default=1024, ge=256, le=4096)


class EditSettings(BaseModel):
    autosave_seconds: int = Field(default=30, ge=5, le=600)
    backup_on_save: bool = True
    max_undo_depth: int = Field(default=50, ge=5, le=500)


class Settings(BaseModel):
    log_level: str = "INFO"
    log_dir: Path = Path("logs")
    cache_dir: Path = Path("pdf_suite_cache")
    theme: str = "system"
    render: RenderSettings = Field(default_factory=RenderSettings)
    edit: EditSettings = Field(default_factory=EditSettings)
    native_accel: bool = True