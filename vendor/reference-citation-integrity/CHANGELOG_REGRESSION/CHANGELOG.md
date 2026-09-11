# RCI version history

## 0.1.0 — 2026-08-13 — initial executable package

- Preserved the supplied `MWM-RCI-SPEC` v0.1.0-draft as `01_SPECIFICATION.md`.
- Added a versioned authority hierarchy, 23 rule IDs across the base ruleset and addendum, source taxonomy, and explicit open-decision hooks.
- Added executable `SKILL.md` instructions for RCI-01 through RCI-07, release gating, evidence preservation, and cross-family handoffs.
- Added validated contracts for the run manifest, citation/reference records, findings, source ledger, decisions, run result, and cross-family boundaries.
- Added `MWM-RCI-EVAL-01` with 51 synthetic fixtures: 6 clean, 15 single-error, 12 adversarial, 10 negative controls, and 8 integration cases.
- Added deterministic suite validation and candidate scoring.
- Added regression intake and production-failure capture schemas/templates. No production failure is claimed by this package.

### Open at release

The package intentionally leaves MWM decisions unresolved where the governing specification does: APA edge-case adoption, dataset identifier fallbacks, source-of-record conflicts, access-date policy, source relations, auto-fix whitelist, notes/endnotes scope, software policy, and provider-match thresholds. Runtime behavior is to preserve evidence and escalate, block, or return not-ready as specified.

## 2026-08-14 packaging update

- Added `01_SPECIFICATION.docx` as a source-preserving Word version of the governing specification. The Markdown specification remains the design authority; no editorial rule or open MWM decision was changed.

## Change policy

Use semantic versioning. A major change alters rule hierarchy, output schemas, or intervention authority. A minor change adds a backward-compatible source type, detection rule, or evaluation coverage. A patch change corrects wording, locators, or nonbehavioral metadata. Every behavior change requires at least one gold fixture and a regression entry before release.
