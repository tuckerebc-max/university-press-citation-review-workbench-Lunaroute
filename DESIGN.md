# University Press Workbench Design

## Outcome

The workbench implements the previously selected federated model: University Press owns the professional constitution and acceptance authority; the Navy Yard Workbench Foundry designs and maintains the executable system; each run compiles an immutable, policy-bound plan.

The design carries four records through every batch:

1. A source manifest with stable chapter IDs, relative paths, sizes, and SHA-256 hashes.
2. An immutable execution plan with provider approval, classification, stage order, skill commits, model, concurrency, and prohibited effects.
3. Per-chapter evidence and author packets that preserve raw values and distinguish observed text, candidate metadata, model proposals, and human decisions.
4. A run receipt and append-only observation stream that reconcile every completed packet to the source manifest without fabricating acceptance.

## Execution sequence

```text
folder scan
  -> source hashes and provider approval
  -> immutable plan
  -> deterministic DOCX or text extraction
  -> citation and reference inventory
  -> optional fixed-host Crossref candidates
  -> reference-citation-integrity review
  -> scholarly-editorial-integrity review
  -> neutral author comments and queries
  -> chapter receipt
  -> run reconciliation and human acceptance queue
```

Reference and Citation Integrity always runs first. Scholarly and Editorial Integrity receives the RCI result and citation-graph status. A source hash is checked before extraction, before each external model stage, and after the author packet is produced. A mismatch blocks that chapter.

## Fixed and adaptive decisions

Fixed invariants are source preservation, stage order, version pins, explicit provider approval, strict model-output schemas, neutral integrity language, visible exceptions, human acceptance, and no publication. Navy Yard may adapt the approved GLM 5.3 variant, bounded concurrency, chapter ordering, and optional Crossref candidate lookup.

## Author packet design

The distributable chapter copy does not silently accept edits. Word comments attach a finding to a paragraph where possible; a final review appendix makes every proposed change and query visible even when a document's XML structure prevents comment anchoring. The accompanying Markdown query sheet and script-free HTML view give authors low-friction alternatives.

## Current pilot boundary

This release is a bounded preview pilot. It supports local DOCX, Markdown, and UTF-8 text chapters. It does not ingest PDFs, download arbitrary URLs, inspect full source articles, modify live editorial systems, accept edits, or publish. Those capabilities require separate policies and tests.
