# Contributing to pdf-reader-editor-suite

Thanks for wanting to push the PDF tooling forward. This repo is a
community-maintained Windows desktop reader/editor with a Python core and
optional native accelerators (C++, C#, Java) for rendering, text extraction,
and structured content editing.

## Ground rules

- Target Python **3.12+** on Windows 10/11 x64. Linux/macOS builds are
  best-effort via the same package tree.
- Every PR that touches `src/pdf_suite/render`, `src/pdf_suite/extract`, or
  `src/pdf_suite/edit` must include at least one test under `tests/`.
- Keep new dependencies pinned in `pyproject.toml`. No floating `*` versions.
- Native modules go under `native/` and must ship a CMake or MSBuild file.
  Python-facing wrappers live in `src/pdf_suite/native_bridge/`.

## Local dev setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev,native]"
pre-commit install
pytest -q
```

## Style

- `ruff` for lint + format, `mypy --strict` on `src/pdf_suite`.
- Docstrings on every public callable. Google style.
- No bare `except:` — catch `PdfSuiteError` subclasses or re-raise.

## Branch / commit

- Branches: `feat/<area>-<short>`, `fix/<area>-<short>`, `native/<lang>-<short>`.
- Commits: Conventional Commits (`feat(edit): add annotation layer merge`).

## Reporting issues

Include: Windows build number, Python version, PDF sample (redacted if
needed), and the exact traceback. Attach `logs/pdf_suite.log` when possible.