# Vendored package patches

## scholarly-editorial-integrity

The upstream commit is pinned in `skills.lock.json`. A semantic portability patch is applied to `scripts/validate_package.py`: governed Markdown is normalized from CRLF to LF before its SHA-256 is compared with the upstream canonical hash. A normal Windows checkout otherwise reports a false integrity failure even though its Git-normalized content matches the pinned commit.

No specification, rule, schema, fixture, or operating instruction is changed.
