# Architecture

```
pdf_suite/
├── app/            # bootstrap, lifecycle, shell
├── cli/            # headless typer app
├── config/         # pydantic schema + loader
├── core/           # document + page model (pikepdf)
├── handlers/       # one module per user op
├── native_bridge/  # ctypes loaders for C++/C#/Java
├── services/       # document registry, render cache, OCR
└── utils/          # logging, path safety
```

Flow: `__main__` → `bootstrap` → `Lifecycle.run` → `Shell`. The shell
picks Qt when available, otherwise falls through to `cli.app`. Handlers
are the only layer allowed to touch services; services are the only layer
allowed to touch core. Core never imports services.

Sandbox: `utils.paths.ensure_within` gates every embedded-file extraction.
The JS action interpreter lives in `services` and is wall-clock capped at
200 ms per action.