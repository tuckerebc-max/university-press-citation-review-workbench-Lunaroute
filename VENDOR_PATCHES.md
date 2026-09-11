# Vendored package patches

## scholarly-editorial-integrity

The upstream commit is pinned in `skills.lock.json`. A semantic portability patch is applied to `scripts/validate_package.py`: governed Markdown is normalized from CRLF to LF before its SHA-256 is compared with the upstream canonical hash. A normal Windows checkout otherwise reports a false integrity failure even though its Git-normalized content matches the pinned commit.

No specification, rule, schema, fixture, or operating instruction is changed.

The workbench's outer package lock uses the same checkout-independent rule for UTF-8 text files: CRLF is canonicalized to LF before each file digest is added to the tree hash. Binary files remain byte-exact. This prevents Git line-ending settings from invalidating an otherwise identical pinned package.
