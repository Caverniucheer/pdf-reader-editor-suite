"""pdf-reader-editor-suite: modular Windows PDF reader and editor.

Public surface intentionally small. Reach into subpackages for anything
beyond the app bootstrap and the shared error hierarchy.
"""

from pdf_suite.errors import (
    PdfSuiteError,
    ParseError,
    RenderError,
    EditError,
    SandboxViolation,
)
from pdf_suite.version import __version__

__all__ = [
    "__version__",
    "PdfSuiteError",
    "ParseError",
    "RenderError",
    "EditError",
    "SandboxViolation",
]