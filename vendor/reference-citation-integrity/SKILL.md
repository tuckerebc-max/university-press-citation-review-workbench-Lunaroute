---
name: reference-citation-integrity
description: Inspect and reconcile a manuscript's citations, references, source identity, metadata, DOI/URL records, and APA/MWM rendering with evidence-backed findings and release status. Use when Codex needs a baseline, incremental, full, release, or proof-stage RCI review; do not use it for claim support, substantive fact-checking, permissions, copyediting, or developmental editing.
---

# Reference & Citation Integrity

Run the RCI family as an evidence-preserving pipeline. Treat `01_SPECIFICATION.md` as the design authority, `02_RULES/` as the versioned rule/configuration layer, `schemas/` as output contracts, `evals/` as the acceptance suite, and `CHANGELOG_REGRESSION/` as the maintenance record.

## Execute

1. Load the run manifest, active project profile, exception/decision register, prior unresolved findings, rule-set version, and renderer version. Validate the manifest against `schemas/run-manifest.schema.json`.
2. Stop a release claim when a precondition fails. Return `not_ready` with a specific reason; a partial baseline inventory may still be produced.
3. Parse the manuscript without losing structure. Inventory body paragraphs, headings, notes, tables, captions, appendices, supplementary material, reference-list boundaries, hyperlinks, visible URLs/DOIs, and stable locators. Preserve every raw extracted value.
4. Normalize citation instances (`C...`) and reference entries (`R...`) without overwriting raw text. Preserve context type, author/group author, year/date, locator, source type, identifiers, and parse confidence.
5. Establish source identity and source type before applying formatting. Keep preprints, published articles, datasets, software releases, versions, corrections, translations, and related works distinct unless evidence and an editorial decision support a relation.
6. Reconcile in this order: stable identifier or decisive key; group-author/year and title; author/year/title plus container or identifier; provider candidate; human review for multiple plausible candidates. Never confirm a match from title similarity alone.
7. Verify material metadata and identifiers field by field. Preserve raw, normalized, observed, evidence, and rendered values. Treat provider metadata as candidate evidence, not a verdict. Record retrieval time, source URL/locator, and access status.
8. Render only after identity and required metadata checks. Use the pinned MWM/APA rule package and deterministic renderer where available. Apply the project exception layer explicitly and record rule, renderer, and exception versions.
9. Run anomaly checks across all in-scope contexts: missing/orphan links, duplicates, collisions, source-type mismatch, DOI mismatch, related-work confusion, missing required identifiers, incomplete source structures, quotation locators, coverage gaps, and renderer regression.
10. Emit findings that include location, raw/normalized values, rule ID, evidence, confidence, action, status, dependencies, and decision-log reference. Validate findings with `schemas/finding.schema.json`.
11. Apply only the action permitted by the active decision hooks. Default unresolved policy decisions to `FLAG`, `ESCALATE`, or `BLOCK` as specified; never invent a MWM exception or silently substitute, merge, delete, or repair identity-bearing metadata.
12. Rerun inventory and reconciliation after approved corrections. Produce a run result and release status; RCI reports readiness to Editorial QA & Orchestration but does not authorize publication.

## Skill routing

Use the bounded subskill that answers the request:

- `RCI-01`: citation-to-reference matching and relationship ledger.
- `RCI-02`: missing citations, orphan references, and exception coverage.
- `RCI-03`: source identity and field-level metadata evidence.
- `RCI-04`: source-type-specific MWM/APA construction and rendering.
- `RCI-05`: DOI/URL syntax, resolution, identity comparison, and access status.
- `RCI-06`: in-text/reference formatting and renderer regression.
- `RCI-07`: duplicate, collision, related-work, and source-integrity anomalies.
- Release mode: run `RCI-01` through `RCI-07` in order, rerun dependent checks after approved changes, then apply the release gate.

## Boundaries and handoffs

Do not decide whether a source supports a claim, whether a claim is true, whether a source is prestigious or ideologically adequate, whether a new source should be added, or whether permissions/ethics are satisfied. Route claim-to-source fit, quotation verification, author/organization facts, and unsupported assertions to Scholarly/Editorial Integrity. Route house-style choices to Style-Guide Implementation. Route sentence-level intervention to Copyediting. Route structural completeness and release sequencing to Chapter Completeness & Production Readiness and Editorial QA & Orchestration. Route post-typesetting preservation checks to Proof & Post-Typesetting Review.

RCI may provide downstream families with source identity, metadata provenance, citation/reference relationships, identifier status, findings, and release conditions. Downstream families must not reinterpret an RCI identity finding as claim-support evidence or silently replace the source record.

## Required output

Return a validated run result using `schemas/run-result.schema.json`, plus the normalized ledger and decision records when applicable. Use only these release dispositions: `ready`, `ready_with_conditions`, or `not_ready`. Use the fixed action vocabulary: `AUTO_FIX`, `SUGGEST`, `FLAG`, `ESCALATE`, `BLOCK`, `CLOSE`. Use the fixed status vocabulary from the specification. If evidence is missing, state the gap and lower confidence; never replace it with model memory.

## Acceptance check

Before handoff, run the RCI evaluator in `evals/` and the package validator in `scripts/validate_package.py`. All clean controls must remain clean, critical fixtures must detect the expected rule, unresolved project decisions must remain explicit, and no material identity change may be marked automatic without an enabled decision hook.
