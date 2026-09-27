"""Locate and load native accelerator modules. Degrades gracefully."""

from __future__ import annotations

import ctypes
import platform
from pathlib import Path

from pdf_suite.errors import NativeModuleUnavailable
from pdf_suite.utils.logging import get_logger

log = get_logger(__name__)

_BACKENDS = {
    "Windows": "pdf_suite_native.dll",
    "Linux": "libpdf_suite_native.so",
    "Darwin": "libpdf_suite_native.dylib",
}


class NativeLoader:
    """Loads the optional C++ render accelerator.

    Missing accelerator is not fatal — the pure-Python path is the fallback.
    """

    def __init__(self, search_dir: Path | None = None) -> None:
        self._dir = search_dir or Path(__file__).resolve().parent
        self._handle: ctypes.CDLL | None = None

    def load(self) -> ctypes.CDLL:
        if self._handle is not None:
            return self._handle
        name = _BACKENDS.get(platform.system())
        if name is None:
            raise NativeModuleUnavailable(f"no native backend for {platform.system()}")
        path = self._dir / name
        if not path.exists():
            raise NativeModuleUnavailable(f"native module missing: {path}")
        self._handle = ctypes.CDLL(str(path))
        log.info("loaded native accelerator %s", path.name)
        return self._handle

    @property
    def is_available(self) -> bool:
        try:
            self.load()
        except NativeModuleUnavailable:
            return False
        return True