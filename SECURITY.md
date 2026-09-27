# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security-only |
| < 0.3   | no        |

## Reporting a vulnerability

Email `security@pdf-suite.dev` (PGP key in `docs/pgp.txt`) or open a
private advisory on GitHub. Do **not** file public issues for:

- Malformed-PDF parsing that leads to arbitrary code execution
- Sandbox escapes in the JS/action stream interpreter
- Path traversal in embedded-file extraction
- Signature bypass in incremental save

We aim to acknowledge within 72 hours and ship a patch release within 14 days.

## Threat model notes

The reader parses untrusted PDFs. Assume the input is hostile. The
`pdf_suite.sandbox` module runs the JS action interpreter with a
restricted builtin set and a hard 200 ms wall-clock budget per action.
Embedded file extraction is confined to a per-document temp dir and
rejects any path that resolves outside it after NTFS normalization.

## Out of scope

- Rendering fidelity bugs (open a normal issue)
- Crashes on malformed PDFs without a security impact
- Issues in third-party native modules that already have upstream advisories