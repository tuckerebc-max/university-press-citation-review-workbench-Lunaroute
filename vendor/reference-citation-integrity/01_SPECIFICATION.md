# Modeling What Matters Editorial Skills
## Reference & Citation Integrity — Operational Skill-Family Specification

**Specification ID:** `MWM-RCI-SPEC`  
**Version:** `0.1.0-draft`  
**Corpus ID:** `MWM-RCI-2026-08`  
**Status:** Draft for editorial review  
**Prepared:** August 13, 2026  
**Scope:** Chapter manuscripts and associated reference materials for *Modeling What Matters*

## 1. Purpose

Reference & Citation Integrity (RCI) is a bounded editorial capability for determining whether a manuscript’s citations, references, source metadata, and persistent identifiers form a coherent, evidence-backed, release-ready system.

RCI does four things in sequence:

1. identifies and normalizes citation and reference records;
2. reconciles their relationships across the manuscript;
3. verifies source identity, metadata, and identifiers against appropriate evidence;
4. renders and reports the result under the adopted MWM/APA rule package.

Its governing invariant is:

> A citation or reference is not release-ready until its source identity, source type, metadata evidence, formatting rule, and relationship to the manuscript have been separately checked.

RCI is designed as an inspectable Skill family, not as a single “fix the references” prompt. Every material decision must be reproducible from the manuscript, source evidence, rule version, and output record.

## 2. Scope and non-goals

### In scope

- reference-list to in-text citation reconciliation;
- missing and orphan citation detection;
- metadata verification and provenance capture;
- APA 7 reference construction under the MWM profile;
- DOI and URL normalization and verification;
- citation and reference formatting;
- citation/source anomalies that can be detected without deciding substantive claim support;
- structured findings, confidence, escalation, and release reporting.

### Out of scope

- developmental editing or argument restructuring;
- deciding whether a source substantively supports a claim;
- unrestricted fact-checking;
- judging the quality, prestige, or ideological adequacy of a source;
- deciding whether the author should cite a source that is not already part of the manuscript’s evidence system;
- silently replacing a source, deleting a reference, or merging related works;
- resolving copyright, permissions, or ethical-use questions except to flag them for the appropriate Skill.

Claim-to-source fit, quotation verification, author names and organizational facts, and unsupported assertions route to Scholarly/Editorial Integrity when they exceed RCI’s identity and metadata checks.

## 3. Trigger and editorial stage

RCI runs at the following points:

| Trigger | Required mode | Purpose |
|---|---|---|
| New chapter intake | Baseline scan | Establish the citation/reference inventory and parser coverage. |
| After substantive author revision | Incremental reconciliation | Detect additions, deletions, changed years, changed source identity, and new unresolved links. |
| Before copyedit close | Full verification | Verify metadata, identifiers, source types, and formatting under the current rule package. |
| Before production handoff | Release validation | Confirm MWM completeness rule, clean high-severity queue, and reproducible output. |
| After author queries | Targeted rerun | Recheck only affected records plus dependent collision, ordering, and rendering rules. |
| After typesetting/proof changes | Proof-integrity check | Confirm that citations, references, links, and locator text survived production changes. |

The Editorial QA & Orchestration family determines which RCI mode runs at each stage. RCI itself reports readiness; it does not authorize publication.

## 4. Inputs

### Required inputs

1. The current manuscript file, preferably DOCX plus a rendered PDF when available.
2. The current reference list and all citations in body text, notes, tables, figures, captions, appendices, and supplementary material.
3. The active MWM project profile and rule package.
4. The project’s exception and decision log.
5. Any supplied source copies, author reference export, or metadata spreadsheet.

### Optional inputs

- publisher or repository landing pages;
- DOI, DataCite, Crossref, ORCID, accession, or repository lookup results;
- prior RCI reports and resolved findings;
- source PDFs, title pages, copyright pages, repository records, software release pages, or dataset landing pages;
- a structured citation export (CSL JSON, BibTeX, RIS, JATS, or equivalent).

### Minimum input manifest

The run manifest must record:

```yaml
run_id: "MWM-RCI-<chapter>-<date>-<sequence>"
manuscript_file: "absolute path or managed file identifier"
manuscript_version: "author or production version"
manuscript_sha256: "optional but recommended"
project_profile: "MWM-APA7-v<version>"
exception_register: "path or decision-log identifier"
source_materials: []
prior_run_id: "null or previous run"
run_mode: "baseline | incremental | full | release | proof"
```

## 5. Authoritative sources and authority boundary

The corpus for this specification is stored in the local project folder:

`Editorial Skills Research Corpus/01_Reference_Citation_Integrity/`

The primary source records are in `03_Crosswalk/corpus_manifest.json`; source capsules are in `02_Extracted_Notes/source_capsules.md`.

| Authority tier | Source family | Use |
|---|---|---|
| 1 — project authority | MWM chapter guidance (S001) and approved MWM decisions | Controls project requirements, exceptions, and release boundaries. |
| 2 — adopted style authority | Versioned MWM APA rule package grounded in the supplied APA guide (S002) and checked against official APA sources (S007–S008) | Controls citation and reference presentation. |
| 3 — source identity and metadata standards | DOI Handbook (S009), DataCite (S015), NLM (S019), JATS4R (S020–S023) | Controls source typing, identity evidence, metadata fields, and relationship semantics. |
| 4 — rendering and implementation standards | CSL (S017–S018), DataCite citation mapping (S016) | Controls deterministic rendering and regression testing. |
| 5 — provider documentation | Crossref (S010–S014) | Supplies candidate metadata, identifier operations, and link-display procedures. |
| 6 — implementation exemplars | AISL guides and review (S003–S005), SEFI template (S006) | Informs reporting, exceptions, completeness, and handoff design; does not override MWM. |

The local capture of the official APA common-reference PDF is an access-gateway HTML response and is not evidence. Official APA URLs remain in the authority registry, and disputed edge cases must be marked for human review rather than presented as settled facts.

## 6. Preconditions and readiness checks

RCI may run a full release check only when:

- the manuscript version is identified;
- the current MWM/APA rule package is identified;
- the parser can inspect body paragraphs and, where applicable, tables, captions, notes, and appendices;
- the reference list boundary is known;
- the project exception register is available or explicitly marked unavailable;
- external lookups, if used, can be recorded with retrieval time and source URL;
- the system can preserve the input record and the output finding record;
- unresolved prior findings are imported rather than silently discarded.

If a precondition fails, RCI returns `not_ready` with a specific reason. It may still produce a baseline inventory, but it must not claim release readiness.

## 7. Skill-family architecture

| Skill ID | Name | Primary question |
|---|---|---|
| `RCI-01` | Citation-reference reconciliation | Does each citation connect to the intended reference record, and vice versa? |
| `RCI-02` | Missing/orphan detection | Are any citations missing references or references uncited under the MWM rule? |
| `RCI-03` | Metadata verification | Does each record have identity and field-level evidence from an appropriate source? |
| `RCI-04` | APA construction | Is the source typed correctly and represented under the MWM APA pattern? |
| `RCI-05` | DOI/URL verification | Is the identifier correctly formed, resolvable, and attached to the correct object? |
| `RCI-06` | Citation formatting | Are in-text citations and reference entries rendered consistently under the pinned rule package? |
| `RCI-07` | Source integrity/anomaly checks | Are there duplicates, collisions, type mismatches, related-work confusions, or impossible metadata patterns? |

The seven Skills share one normalized record model and one finding schema. They may run independently, but the release gate runs them in the sequence shown above.

## 8. Operating principles

1. **Identity before formatting.** Never format a source whose type or identity is unresolved when the uncertainty could change the reference.
2. **Evidence before correction.** A proposed change must show the observed value, the evidence value, the rule, and the reason the change is safe.
3. **Provider data is a candidate, not a verdict.** Crossref, DataCite, and other registries can be incomplete or stale.
4. **Do not invent metadata.** Use `unknown`, `not supplied`, or `needs verification` when evidence is absent.
5. **Separate raw, normalized, and rendered forms.** Preserve what the manuscript said, what the system inferred or normalized, and what it rendered.
6. **Preserve related works.** Preprints, articles, datasets, versions, corrections, translations, and software releases must not be merged merely because they look similar.
7. **Prefer reversible actions.** Automatic changes are limited to deterministic, low-risk transformations and must be logged.
8. **Escalate material uncertainty.** The system is allowed to stop short of a correction.
9. **Coverage includes non-body text.** Tables, captions, notes, appendices, and supplementary files are part of the citation system when the project includes them.
10. **Release status is stricter than local correctness.** A reference may be correctly formatted and still not be release-ready if its identity, relationship, or required identifier is unresolved.

## 9. Rule hierarchy

Rules are evaluated in this order:

1. current MWM authority;
2. adopted APA 7 rule package;
3. approved MWM house-style exception;
4. source-type and metadata standards;
5. rendering and provider implementation rules;
6. model inference.

Model inference cannot override a higher-level rule. When two rules at the same level conflict, emit `RCI-CONFLICT-001` and escalate.

Each operative rule has a stable ID. Initial rule families are:

| Rule ID | Rule |
|---|---|
| `RCI-AUTH-001` | MWM project requirements control project-specific citation/reference decisions. |
| `RCI-AUTH-002` | The active APA rule package controls ordinary in-text and reference-list presentation. |
| `RCI-REC-001` | Every in-text citation must resolve to a reference record unless an approved exception exists. |
| `RCI-REC-002` | Every reference must be cited somewhere in the manuscript’s defined citation scope unless an approved exception exists. |
| `RCI-ID-001` | Source identity must be established before automatic reference construction. |
| `RCI-ID-002` | Provider metadata must be preserved as evidence with source and retrieval information. |
| `RCI-ID-003` | A resolving DOI is not sufficient evidence of a correct bibliographic match. |
| `RCI-TYPE-001` | Source type must be explicit for datasets, software, preprints, reports, chapters, and other non-article objects. |
| `RCI-FMT-001` | Rendered output must use a pinned MWM/APA rule package and renderer configuration. |
| `RCI-FMT-002` | DOI display normalization may not change the underlying identifier. |
| `RCI-ANOM-001` | Similarity is not identity; related works must not be merged without evidence and approval. |
| `RCI-ANOM-002` | A missing required persistent identifier is a release blocker when MWM expressly requires it. |
| `RCI-QA-001` | Every release must pass clean, error, edge-case, and regression fixtures. |

## 10. Procedure

### Step 0 — Initialize the run

Create the run manifest, load the project profile and exception register, record the input version, and import the prior run’s unresolved findings.

Output: run header and precondition status.

### Step 1 — Parse the manuscript without losing structure

Extract, with stable locators:

- body paragraphs;
- headings and section boundaries;
- footnotes/endnotes if present;
- tables and table notes;
- figure captions and notes;
- appendices and supplementary text;
- reference-list entries;
- hyperlinks and visible URLs/DOIs.

Retain the original text for each extracted item. If the parser cannot distinguish a caption from body text or omits a table, emit a parser-coverage warning before reconciliation.

### Step 2 — Normalize citation and reference records

Create stable IDs such as `C001` for citation instances and `R001` for reference entries. Normalization may standardize whitespace, Unicode punctuation, case-insensitive comparison fields, and DOI prefixes, but it must not discard the raw value.

Minimum normalized citation record:

```yaml
citation_id: "C001"
raw_text: "(Nguyen & Patel, 2024)"
location: "body.p12.paragraph4"
context_type: "body | table | caption | note | appendix"
authors_or_group: ["Nguyen", "Patel"]
year: "2024"
locator: null
parse_confidence: 0.98
```

Minimum normalized reference record:

```yaml
reference_id: "R001"
raw_text: "Nguyen, A., & Patel, R. (2024). Title..."
location: "references.item12"
source_type: "journal_article"
authors_or_group: ["Nguyen, A.", "Patel, R."]
date: "2024"
title: "Title"
container_title: "Journal Name"
version: null
identifiers: []
metadata_provenance: []
parse_confidence: 0.94
```

### Step 3 — Establish source identity and type

For each reference, classify the object before formatting it. Use the source artifact when available; otherwise use the strongest appropriate metadata source and mark the evidence limitation.

Minimum source types for the initial release:

- journal article;
- book;
- chapter or contribution in an edited book;
- report or working paper;
- conference presentation/proceedings item;
- dissertation or thesis;
- website/web page;
- dataset;
- software/package/release;
- preprint;
- audiovisual or other nontraditional item;
- unknown/ambiguous.

For a dataset, software item, or preprint, preserve resource type, version, relation, and persistent identifier fields where available. If the record could represent more than one object and the difference changes the citation, escalate.

### Step 4 — Reconcile citations and references

Match in stages:

1. exact stable identifier or exact normalized author-year key;
2. group-author/year and title similarity;
3. author/year/title plus container or identifier;
4. candidate matching from a provider, clearly labeled as candidate evidence;
5. human review when more than one plausible record remains.

Do not use title similarity alone as a confirmed match. Record one-to-one, many-to-one, and one-to-many relationships explicitly. A repeated citation instance may link to one reference; a reference may be cited many times. A single citation string containing multiple works must produce multiple links.

### Step 5 — Verify metadata and identifiers

For every material field, compare:

- the manuscript’s value;
- the cited object’s value, if available;
- publisher or repository evidence;
- Crossref/DataCite/other provider evidence;
- the normalized value used for rendering.

For a DOI or other persistent identifier:

1. preserve the raw identifier;
2. normalize its display without changing the identifier;
3. check syntax;
4. resolve the identifier;
5. retrieve candidate metadata;
6. compare identity fields;
7. record retrieval time and status;
8. route mismatch or ambiguity to a human.

For a URL, record whether it is syntactically valid, reachable at check time, and attached to the intended source. A blocked or stale URL is not the same as a source with no identifier.

### Step 6 — Construct and render the reference

After source identity and metadata checks, apply the source-type-specific MWM/APA pattern. The renderer must preserve the normalized record and log:

- rule package version;
- source-type decision;
- renderer and style version;
- any MWM exception;
- rendered output;
- validation results.

Use CSL or an equivalent deterministic renderer for the baseline when practical. Apply the MWM exception layer explicitly and test it. Never patch a rendered string in a way that loses the underlying rule or record.

### Step 7 — Run anomaly checks

At minimum, test for:

- missing reference and orphan reference;
- duplicate or near-duplicate entries;
- same-author/same-year collisions;
- inconsistent group-author names;
- source-type mismatch;
- DOI resolving to a different work;
- title/date/author contradictions;
- preprint/article confusion;
- missing dataset identifier;
- missing software version or identifier;
- incomplete edited-book chapter structure;
- direct quotation without the required locator under the adopted rule;
- citation instances omitted from tables, captions, notes, or appendices;
- renderer regression.

### Step 8 — Produce findings and route actions

Every finding receives severity, confidence, proposed action, and disposition. The report must distinguish:

- `verified`;
- `informational`;
- `needs_review`;
- `blocked`;
- `not_applicable`;
- `not_checked`.

RCI may propose a change, but the output must make clear whether the change was applied, merely suggested, or escalated.

### Step 9 — Apply the release gate

Release-ready status requires:

- no unresolved high-severity identity or reconciliation findings;
- no missing references or orphan references without approved exceptions;
- MWM-required dataset identifiers present or explicitly escalated;
- all DOI/URL issues either verified, documented as inaccessible, or assigned to a human;
- renderer and rule versions recorded;
- evaluation fixtures passed;
- parser coverage acceptable for the manuscript’s structure;
- an editorial decision log for every material exception.

## 11. Detection logic by Skill

### RCI-01 — Citation-reference reconciliation

**Detect.** Parse each citation instance into an author/year/key representation and compare it to reference records. Test the citation’s context type and whether the match is unique.

**Confirmed match.** Stable identifier or decisive author/year/title/identifier agreement, with no competing candidate.

**Ambiguous match.** Two or more candidates remain, the author/group-author is inconsistent, or source type changes the identity interpretation.

**Intervention threshold.** Never automatically rewrite an author name, year, title, or source type to force a match. Suggest a correction only when the intended reference is unambiguous and the change is reversible.

### RCI-02 — Missing/orphan detection

**Detect.** Compare the set of citation records across all defined manuscript contexts to the set of reference records. Apply documented exceptions only after verifying their scope.

**Blocking conditions.** A citation has no reference, a reference is not cited under `RCI-REC-002`, or a parser coverage gap makes completeness unknowable.

**Non-blocking conditions.** A project-approved front-matter reference or an explicitly permitted further-reading section, provided the exception is recorded and not mislabeled as the chapter’s reference list.

### RCI-03 — Metadata verification

**Detect.** For each field, compare observed and verified values and classify the evidence source.

**Required minimum fields.** Author/creator, date, title, source/container as applicable, source type, and identifier or stable access route when required by MWM/APA.

**Intervention threshold.** Missing metadata produces a flag; conflicting identity metadata produces escalation. Never fill a material field from a low-confidence candidate without labeling it.

### RCI-04 — APA construction

**Detect.** Choose source type, confirm required fields, apply the current MWM/APA pattern, and compare output to expected fixture behavior.

**Intervention threshold.** Auto-fix only deterministic mechanics. A source-type change, author-role change, date change, title change, or version change requires suggestion or escalation.

### RCI-05 — DOI/URL verification

**Detect.** Normalize, syntax-check, resolve, compare metadata, and record access status.

**Status vocabulary.** `not_present`, `malformed`, `normalized`, `resolves_match`, `resolves_mismatch`, `does_not_resolve`, `temporarily_unavailable`, `inaccessible`, `ambiguous`, `not_applicable`.

**Intervention threshold.** Canonical display normalization can be automatic when the identifier string is unchanged. Resolution mismatch is always escalated.

### RCI-06 — Citation formatting

**Detect.** Compare rendered output against the pinned rule package and regression fixtures for author ordering, year, suffixes, punctuation, title/container treatment, locator, and DOI/URL display.

**Intervention threshold.** A formatting-only issue can be suggested or auto-fixed if the rule is deterministic and does not alter identity or meaning. If style rules conflict, emit a conflict finding.

### RCI-07 — Source integrity/anomaly checks

**Detect.** Apply identity, relation, and consistency tests across the whole source set.

**High-risk anomaly classes.** DOI/metadata mismatch, source-type mismatch, same-author/same-year collision, dataset without required persistent identifier, software with unresolved object identity, and related work incorrectly merged.

**Intervention threshold.** No automatic deletion, merging, or substitution. Anomaly checks may recommend a merge review, split review, or source-owner confirmation.

## 12. Intervention thresholds

| Action | Permitted when | Examples | Not permitted when |
|---|---|---|---|
| `AUTO_FIX` | Deterministic, reversible, identity-preserving, and covered by a tested rule | Whitespace cleanup; canonical DOI URL display; deterministic punctuation repair | It changes author, date, title, source type, version, or source identity |
| `SUGGEST` | A likely correction is supported but an editor should confirm | Missing comma; likely author-year suffix; clear group-author abbreviation normalization | Multiple plausible sources or missing decisive evidence |
| `FLAG` | A condition affects review but does not justify a proposed rewrite | URL inaccessible; metadata incomplete; unverified optional field | The issue could cause a wrong source or wrong claim relationship |
| `ESCALATE` | Human judgment is required because identity, meaning, authority, or policy is uncertain | DOI mismatch; preprint/article choice; source-type ambiguity; rule conflict; merge/split decision | Never suppress to meet a clean count |
| `BLOCK` | Release cannot responsibly proceed under current MWM rules | Missing reference; orphan reference; required dataset identifier absent; unresolved high-risk identity conflict | Do not block on a clearly informational formatting preference |

## 13. Output schema

### Run result

```yaml
run_id: "MWM-RCI-chapter-20260813-01"
specification_id: "MWM-RCI-SPEC"
specification_version: "0.1.0-draft"
manuscript_version: "author-v3"
project_profile: "MWM-APA7-v0.1"
run_mode: "full"
started_at: "ISO-8601"
completed_at: "ISO-8601"
preconditions: "pass | partial | fail"
parser_coverage: "high | partial | low"
summary:
  citations_found: 0
  references_found: 0
  confirmed_links: 0
  unresolved_links: 0
  findings_total: 0
  blocking_findings: 0
  escalations: 0
release_status: "ready | ready_with_conditions | not_ready"
rule_package_version: "MWM-APA7-v0.1"
renderer:
  name: "CSL or equivalent"
  version: "version"
  style_id: "style identifier"
evaluation_set: "MWM-RCI-EVAL-01"
findings: []
```

### Finding record

```yaml
finding_id: "RCI-20260813-0001"
skill_id: "RCI-05"
rule_id: "RCI-ID-003"
severity: "critical | high | medium | low | informational"
status: "verified | needs_review | blocked | not_applicable | not_checked"
action: "AUTO_FIX | SUGGEST | FLAG | ESCALATE | BLOCK | CLOSE"
confidence: 0.87
location:
  file: "chapter.docx"
  locator: "body.p12.paragraph4 or references.item12"
  context_type: "body | table | caption | note | appendix | reference_list"
observed:
  raw_text: "..."
  normalized_value: "..."
expected:
  value: "..."
evidence:
  - evidence_id: "E006"
    source_id: "S012"
    locator: "Crossref Display Guidelines"
    retrieved_at: "ISO-8601"
    relevance: "canonical DOI display"
provenance:
  source_of_record: "cited object | publisher | registry | author | unknown"
  retrievals: []
reason: "Plain-language explanation of the finding."
proposed_change: "What would change, if any."
dependencies: ["RCI-01 finding ID if reconciliation is affected"]
human_decision: null
decision_log_id: null
```

### Normalized source record

```yaml
source_record_id: "R001"
source_type: "journal_article"
raw_reference: "..."
identity:
  creators: []
  group_author: null
  title: "..."
  container_title: "..."
  date: "..."
  version: null
  edition: null
identifiers:
  - type: "DOI"
    raw: "doi:10.xxxx/abc"
    normalized: "https://doi.org/10.xxxx/abc"
    status: "resolves_match"
metadata_evidence: []
relations: []
rendered_reference: "..."
rendering:
  rule_package: "MWM-APA7-v0.1"
  renderer: "..."
  renderer_version: "..."
  exceptions: []
verification_status: "verified | partial | ambiguous | blocked"
```

## 14. Evidence requirements

Every material finding must be reproducible from:

- exact manuscript location;
- raw observed text or record;
- normalized value used by the check;
- applicable rule ID;
- source or standard evidence;
- retrieval date/version for external lookups;
- proposed action and why it is within or outside automatic authority;
- confidence and uncertainty note;
- final disposition and decision-log reference when human-reviewed.

“The model thinks this is wrong” is not acceptable evidence.

## 15. Confidence and uncertainty

Confidence describes the reliability of the detection or match, not the truth of the source itself:

| Band | Range | Typical condition | Allowed action |
|---|---:|---|---|
| High | 0.95–1.00 | Exact identifier match, deterministic parser, no conflict | Close or auto-fix a safe formatting issue |
| Strong | 0.80–0.94 | Strong match with one nonmaterial gap | Suggest or routine review |
| Moderate | 0.60–0.79 | Plausible candidate or interpretation with ambiguity | Flag; no auto-fix |
| Low | <0.60 | Multiple plausible sources, parser failure, or source-type uncertainty | Escalate |

The system must lower confidence when any of the following is true:

- source type is inferred rather than evidenced;
- title, date, author, or identifier fields conflict;
- a provider match is the only support;
- the input occurs in a table, caption, note, or nonstandard layout;
- a related-work relationship could change the editorial meaning;
- the applicable rule is not in the current MWM/APA package.

## 16. Human-escalation rules

Escalate when:

1. two or more source identities remain plausible;
2. a DOI resolves but the landing object does not match the manuscript record;
3. changing the source type would change author, date, title, version, or relation fields;
4. a preprint, article, correction, translation, dataset version, or software release might be intentionally distinct;
5. official sources and provider metadata disagree on a material identity field;
6. a required identifier is absent and the accepted fallback is not defined;
7. the rule package and the manuscript’s explicit author/editor decision conflict;
8. the parser cannot establish whether a citation is in scope;
9. deleting, merging, or substituting a reference would change attribution, reproducibility, or claim context;
10. an RCI finding appears to require a substantive judgment about claim support.

The escalation record must name the decision requested, the evidence already collected, the plausible alternatives, and the consequence of each alternative.

## 17. Tool and model routing

| Task | Preferred capability | Model role |
|---|---|---|
| DOCX/HTML/PDF extraction | Structured document parser | Deterministic extraction; preserve locators and raw text |
| Citation/reference graph | Rule-based normalizer and graph builder | Deterministic first pass; model resolves only ambiguous syntax |
| DOI/registry lookup | Crossref/DataCite/DOI retrieval with provenance | Provider returns candidates; model compares evidence |
| Source-type classification | Rule-based taxonomy plus constrained model | Model may propose type; human decides material ambiguity |
| Reference rendering | CSL or pinned equivalent renderer | Deterministic baseline; model does not invent formatting |
| Anomaly review | Rules plus model explanation | Model explains evidence and options; does not silently adjudicate |
| Final release check | Independent QA pass | Separate reviewer or model compares findings to gold fixtures |

For ambiguous or high-impact cases, use two independent judgments and route disagreements to a human editor. The orchestration layer records which tool/model produced each field.

## 18. QA and evaluation

The evaluation set is stored at:

`04_Evaluation_Set/evaluation_set.md`

Evaluation set ID: `MWM-RCI-EVAL-01`.

It includes clean controls, single-error fixtures, source-type edge cases, identifier failures, related-work cases, non-body citations, and renderer regressions. Required release coverage includes:

- clean journal article;
- missing and orphan citation;
- same-author/same-year collision;
- group author;
- DOI normalization, nonresolution, and metadata mismatch;
- URL-only and inaccessible web source;
- dataset with and without persistent identifier;
- software with clear and ambiguous identity;
- preprint/article relation;
- book/chapter/report source-of-record conflict;
- no-date source;
- quotation locator;
- table/caption/note coverage;
- duplicate reference;
- renderer regression.

### QA gates

**Gate A — corpus integrity**

- manifest parses;
- local files and URLs have provenance records;
- access failures are labeled and excluded from evidence claims;
- source capsules and crosswalk are internally consistent.

**Gate B — rule integrity**

- every automatic rule has a stable ID;
- every high-severity rule names evidence and escalation conditions;
- MWM/APA conflicts are explicit;
- non-goals prevent scope drift into substantive editing.

**Gate C — output integrity**

- every finding has location, rule, evidence, action, confidence, and status;
- normalized and rendered records remain linked;
- no finding recommends a material identity change without escalation.

**Gate D — regression integrity**

- all clean controls remain clean;
- all critical fixtures detect the expected issue;
- renderer version and expected output are recorded;
- every new MWM exception adds a fixture.

## 19. Examples and counterexamples

### Example 1 — safe DOI display normalization

**Observed:** `doi:10.1234/abc`  
**Evidence:** identifier string is unchanged; the project adopts canonical DOI URL display.  
**Action:** `AUTO_FIX` to `https://doi.org/10.1234/abc`; preserve the raw value in the record.

### Counterexample 1 — unsafe DOI replacement

**Observed:** DOI resolves to a title that resembles but does not equal the reference.  
**Incorrect action:** replace the reference metadata with the DOI landing-page metadata.  
**Correct action:** `ESCALATE` with both records and an identity-mismatch finding.

### Example 2 — missing dataset identifier

**Observed:** chapter cites a dataset by author/title/date but supplies no DOI, accession number, repository identifier, or stable URL.  
**Evidence:** MWM guidance requires a persistent identifier for datasets.  
**Action:** `BLOCK` or `ESCALATE` depending on whether an identifier can be obtained from the source owner.

### Counterexample 2 — invented dataset identifier

**Incorrect action:** infer a DOI from a similarly titled DataCite record.  
**Correct action:** retain `identifier_status: missing` and request source confirmation.

### Example 3 — uncited reference

**Observed:** a reference appears in the chapter’s reference list but no citation is found in body, notes, tables, captions, or appendices.  
**Action:** `BLOCK` under `RCI-REC-002` unless an approved exception is recorded.

### Counterexample 3 — deleting before checking coverage

**Incorrect action:** delete the reference because a body-text search found no match.  
**Correct action:** confirm parser coverage for tables, captions, notes, and appendices first.

### Example 4 — preprint and article

**Observed:** a preprint and later journal article share authors and a similar title.  
**Action:** preserve both until the editor confirms which work the chapter intended; report a related-work review, not an automatic duplicate.

### Counterexample 4 — similarity equals identity

**Incorrect action:** collapse both records because title similarity exceeds a threshold.  
**Correct action:** compare source type, publication state, identifiers, dates, and editorial intent.

### Example 5 — formatting-only APA correction

**Observed:** a reference has a deterministic punctuation error while identity and fields are verified.  
**Action:** `AUTO_FIX` or `SUGGEST`, depending on the project’s approved auto-fix list, with renderer evidence.

### Counterexample 5 — formatting used to hide missing metadata

**Incorrect action:** render a polished reference with an inferred date or publisher.  
**Correct action:** show the missing field, cite the evidence gap, and escalate if material.

## 20. Failure modes and mitigations

| Failure mode | Consequence | Required mitigation |
|---|---|---|
| Parser omits tables/captions/notes | False orphan-reference or missing-reference findings | Coverage check and structured-location inventory |
| DOI resolves to wrong object | Wrong source attribution | Metadata comparison and mandatory escalation |
| Provider metadata copied blindly | Silent author/title/date corruption | Field-level provenance and source-of-record hierarchy |
| Group author split into personal authors | Incorrect in-text form and attribution | Preserve group-author role; require evidence for expansion |
| Same-year suffixes assigned inconsistently | Citation ambiguity | Recompute ordering globally and test affected citations |
| Preprint/article merged | Reproducibility and version error | Typed source relations; no automatic merge |
| Dataset/software treated as journal article | Missing identifier/version/relationship data | Typed-source minimum fields and edge-case rules |
| URL outage interpreted as source absence | Unnecessary deletion or blocking | Separate access status from source identity status |
| Renderer changes without fixture update | Silent style drift | Pin versions and run regression tests |
| APA access failure treated as complete coverage | Overconfident edge-case decisions | Authority registry and explicit maintenance/gap status |
| Model over-edits author text | Meaning or voice changes | Limit RCI to citations/references and deterministic mechanics |
| Human decision not recorded | Same ambiguity recurs | Decision log ID required for material escalation closure |

## 21. Versioning and maintenance

### Version format

Use semantic versioning:

- **major** — rule hierarchy, output schema, or intervention authority changes;
- **minor** — new source type, detection rule, or evaluation coverage that is backward-compatible;
- **patch** — wording, locator, or nonbehavioral correction.

### Versioned assets

Every release must pin:

- specification version;
- MWM/APA rule package version;
- exception-register version;
- renderer/style/processor version;
- corpus manifest version;
- evaluation-set version;
- external lookup date or snapshot identifier when available.

### Maintenance triggers

Review the package when:

- MWM guidance changes;
- APA rules or official examples change;
- a new source type is added to the project;
- a provider changes API or metadata behavior;
- an evaluation fixture fails;
- a human editor reverses an automatic action;
- production or proof review discovers a missed citation/reference defect.

The local corpus records access failures and unresolved decisions in `verification_queue.md`. A question becomes a rule only after editorial adjudication, a stable rule ID, and a regression fixture are added.

## 22. Release checklist

Before marking an RCI run `ready`:

- [ ] Manuscript version and run manifest are recorded.
- [ ] Parser coverage includes body text and all in-scope non-body content.
- [ ] Every citation instance has a reference link or approved exception.
- [ ] Every reference is cited or has an approved exception.
- [ ] Source types are classified, with ambiguous cases escalated.
- [ ] Required metadata is verified or explicitly marked missing.
- [ ] Dataset identifiers meet MWM requirements.
- [ ] DOI/URL status is recorded and material mismatches are escalated.
- [ ] Rendering uses pinned rule and renderer versions.
- [ ] No high-severity anomaly remains unresolved.
- [ ] Findings contain evidence, location, rule, confidence, action, and status.
- [ ] Evaluation fixtures pass.
- [ ] Human decisions and MWM exceptions are logged.
- [ ] The output is handed to Editorial QA & Orchestration for stage-level release validation.

## 23. Open decisions for editorial adjudication

The following questions remain intentionally open and are tracked in the research corpus verification queue:

- exact MWM adoption of APA edge cases not specified in the chapter guidance;
- access-date policy for web sources;
- accepted persistent-identifier fallbacks for datasets;
- source-of-record hierarchy for material metadata conflicts;
- auto-fix whitelist;
- structured intermediate format for future production exchange;
- note/endnote treatment across manuscript types;
- software-reference policy;
- minimum Crossref/DataCite evidence threshold for accepting a probable match;
- representation of versions, corrections, translations, preprints, and related works.

RCI is complete only when these questions are either resolved in the project decision log or explicitly marked as human-review conditions in the release profile.

## 24. Research basis

The specification is grounded in the local corpus and crosswalk:

- `03_Crosswalk/corpus_manifest.json`
- `02_Extracted_Notes/source_capsules.md`
- `03_Crosswalk/evidence_crosswalk.md`
- `03_Crosswalk/exemplar_comparison_and_gaps.md`
- `03_Crosswalk/verification_queue.md`
- `04_Evaluation_Set/evaluation_set.md`

The corpus’s central synthesis is that high-quality reference work combines project authority, source identity evidence, structured metadata, deterministic rendering, inspectable findings, and regression testing. No individual external standard is treated as a complete substitute for the MWM editorial decision system.

