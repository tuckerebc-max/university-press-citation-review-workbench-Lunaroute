---
name: scholarly-editorial-integrity
description: Conduct evidence-first scholarly and editorial integrity review of claims, sources, quotations, paraphrases, source status, overlap signals, authorship/contributorship records, disclosures, internal consistency, AI use, confidentiality, serious concerns, and decision logs without inferring intent, misconduct, authorship entitlement, conflict, legal status, or source truth from prose alone. Use for MWM integrity review, case routing, release gates, or evidence-preserving decisions; do not use for citation identity alone, copyediting, technical objects, or institutional adjudication.
---

# Scholarly/Editorial Integrity

Run CEI as a signal, evidence, ownership, remedy, and decision-log workflow.
Treat `01_SPECIFICATION.md` as design authority, `02_RULES/` as the versioned
integrity rule/configuration layer, `schemas/` as contracts, `evals/` as
acceptance tests, and `CHANGELOG_REGRESSION/` as the maintenance record.

## Execute

1. Load chapter/version, stage/trigger, MWM decisions, RCI citation graph
   status, source and status records, contributor/declaration records, source
   access and confidentiality policy, chapter profile, prior findings,
   responses, tools, and assigned owner. Validate the run manifest.
2. Return `blocked` or `source_unavailable` when identity, stage, delegated
   authority, confidentiality permissions, citation graph, source-access log,
   case ownership, or approved-tool status is missing. Do not compensate with
   model confidence.
3. Inventory atomic claims, citations, quotations, paraphrases, names, dates,
   numbers, tables, contributor/byline records, funding/conflict/ethics/
   consent/data/code/AI disclosures, source-status fields, and version links.
4. Protect quotations, participant details, author correspondence, allegations,
   reviewer material, confidential manuscripts, raw data, contact information,
   and legal/ethics records. Do not send protected inputs to an unapproved tool.
5. Run deterministic identity/status/disclosure/consistency checks, then
   source-comparison checks for scope, certainty, modality, causality,
   attribution, quotation fidelity, and version. Record access status exactly.
6. Treat overlap, authorship, disclosure, ethics, AI, source-status, and
   contradiction results as signals or queries. Never infer intent, plagiarism,
   misconduct, authorship entitlement, conflict of interest, legal status, or
   truth from a score, style, affiliation, or model judgment.
7. Classify risk by centrality, interpretation/credit effect, public/legal/
   ethical/confidentiality risk, evidence quality, and reversibility. Choose
   pass, query, qualify, correct, replace_source, hold, refer, notice, or block.
8. Emit findings with exact text/locator, object type, source/record, access
   status, comparison basis, authority, neutral reason, owner, next action,
   confidence, escalation, response, closure condition, and release effect.
9. Preserve original findings and responses. Reassess without erasing the
   evidence trail; close only with an authorized decision record and closure
   evidence. No-change is a valid result.
10. Route RCI metadata/identity, TE objects, SGI language policy, CE sentence
    mechanics, CPR completeness, PPR proof, institutional/ethics/legal,
    publisher/source-owner, and security/privacy questions to their owners.
11. Apply release gate: no unresolved high/critical case, central
    source-unavailable quotation, disputed authorship change, confidentiality
    incident, materially stale source, missing mandatory disclosure, or
    unapproved public-status remedy remains open.

## Routing

- `CEI-01`: claim-to-source fit.
- `CEI-02`: quotation and paraphrase integrity.
- `CEI-03`: source identity and status.
- `CEI-04`: overlap/plagiarism signal review.
- `CEI-05`: authorship/contributorship signal review.
- `CEI-06`: disclosure and transparency review.
- `CEI-07`: serious concern routing.
- `CEI-08`: internal factual consistency.
- `CEI-09`: editorial AI use and confidentiality.
- `CEI-10`: integrity report and decision log.

## Boundaries

The family does not declare misconduct, plagiarism, fabrication,
falsification, intent, authorship entitlement, author order, conflict of
interest, legal status, ethics-committee outcome, or source truth from prose.
It does not arbitrate disputes or upload confidential content to unapproved
external tools. It preserves disagreement and routes institutional,
publisher, rights, legal/ethics, and security decisions.

## Output and acceptance

Invoke as `$scholarly-editorial-integrity` for evidence-preserving integrity
review or case routing. Return a validated result using
`schemas/run-result.schema.json`, with source-access records, findings,
decisions, responses, and release dependencies as applicable. Use statuses
`verified`, `supported_with_scope`, `signal`, `source_unavailable`, `disputed`,
`referred`, `resolved`, and `blocked`; use interventions `AUTO_RECORD`, `PASS`,
`QUERY`, `QUALIFY`, `CORRECT`, `HOLD`, `REFER`, `BLOCK`, or `NO_ACTION`. Before
handoff, run `evals/scorer.py --validate-suite`, `scripts/validate_package.py`,
and the standard Codex skill validator. No formal allegation may appear
without an authorized human record, and no source-unavailable case may PASS as
verified without evidence.