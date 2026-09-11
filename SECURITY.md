# University Press Workbench Security Review Boundary

## Posture

The workbench handles untrusted manuscript files and sends approved manuscript text to an external model provider. It therefore fails closed around archive structure, path identity, provider approval, source drift, model output shape, network destinations, and release language.

## Implemented controls

- Binds the browser interface only to `127.0.0.1` and rejects non-loopback Host headers.
- Requires a per-process random request token and a same-origin header on every state-changing browser request.
- Sends restrictive CSP, frame, MIME-sniffing, cache, and referrer headers.
- Reads `LUNAROUTE_API_KEY` from the process environment and never writes headers or key values to logs, SQLite, receipts, prompts, or packets.
- Allows network calls only to `gw.lunaroute.com` and, when selected, `api.crossref.org`; rejects non-public DNS results and redirects.
- Never fetches URLs supplied by a manuscript or model.
- Rejects symlinks and Windows reparse points, enforces canonical source and output roots, and generates output names from internal chapter IDs.
- Inspects DOCX archive member paths, duplicates, counts, expanded sizes, compression ratios, and XML declarations before parsing.
- Caps chapter count, individual and total bytes, request bodies, model input characters, workers, retries, response bytes, and model calls.
- Binds provider approval to the exact source manifest hash and re-hashes a chapter before every external stage.
- Sends chapter text only as an explicitly delimited untrusted data object and gives the model no tools.
- Rejects schema-invalid model output without coercion.
- Enforces source-unavailable and neutral-language rules after model output.
- HTML-escapes all author-facing values and produces script-free review HTML.
- Writes every model proposal as a comment or query; human acceptance and publication remain unreachable from the application.

The static Bandit check skips B606 for the single guarded `os.startfile` call used by the user-facing **Open output folder** button. The target comes from a validated, workbench-owned run record; no command string or shell is involved.

## Residual risk

No local review proves a system secure. Remaining risks include model behavior drift, parser gaps in unusual Word documents, provider compromise, operating-system compromise, inaccurate but schema-valid model findings, and the draft status of both integrity policies. Run only on chapter sets whose provider path has been approved. A press editor must review every author packet and all high-risk or blocked findings.

## Private reporting and credentials

Do not place credentials or confidential chapter text in a public issue. If an API key appears in a filename, task title, log, or repository, preserve the evidence and have the credential owner rotate it through LunaRoute. Removing text from a current file does not revoke a key or remove historical copies.
