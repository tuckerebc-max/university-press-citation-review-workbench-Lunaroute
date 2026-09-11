# Scholarly/Editorial Integrity Specification

**Specification ID:** `MWM-SEI-SPEC`  
**Version:** `0.1.0-draft`  
**Status:** Draft for editorial-owner review  
**Skill family:** Scholarly/Editorial Integrity  
**Research corpus:** `MWM-SEI-2026-08`  
**Scope:** Edited scholarly chapters; manuscript and production stages before final release  
**Out of scope:** Institutional research-misconduct investigations, authorship arbitration, legal determinations, ethics-committee decisions, and source-verification guarantees  
**Last revised:** August 13, 2026

## 1. Purpose

The Scholarly/Editorial Integrity family checks whether a chapter’s claims, sources, quotations, contributor statements, disclosures, and publication-status signals are responsibly represented and ready for editorial release. It creates an evidence-preserving signal, query, routing, and decision-log system.

The family must improve the reliability and transparency of the scholarly record without pretending that a text model can determine intent, deception, plagiarism, authorship entitlement, conflict of interest, or research misconduct from prose alone.

### 1.1 Non-negotiable boundary

The Skill may:

- identify an observable anomaly or omission;
- compare a claim, quotation, or metadata field with an available source;
- classify evidence quality and source-access status;
- ask an author or editor for a response;
- recommend a correction, qualification, source replacement, hold, or referral;
- preserve a case record and link related versions.

The Skill may not:

- declare an author guilty of misconduct, plagiarism, fabrication, or falsification;
- infer intent, knowledge, recklessness, deception, or bad faith from style, confidence, or model judgment;
- decide who deserves authorship or the order of authors;
- infer a conflict of interest from an affiliation, employer, topic, or funding relationship;
- invent a quotation, locator, source record, DOI, status, author response, or institutional finding;
- treat a similarity score as a plagiarism finding;
- upload confidential manuscript content into an unapproved external service;
- silently change a meaning-bearing claim, quotation, disclosure, contributor statement, or source status.

## 2. Triggers

| Trigger | Required action | Default mode |
|---|---|---|
| Intake baseline | Build a source/claim/contributor/disclosure inventory and surface high-risk signals. | Full scan |
| Citation/reference review complete | Consume the resolved citation graph and inspect source fit, quotations, and status. | Targeted |
| Author or editor raises a concern | Preserve the allegation, request evidence, and route by issue type. | Case review |
| Author response or source evidence arrives | Reassess the finding without erasing prior evidence. | Recheck |
| Correction, retraction, expression of concern, or status change | Update version/status lineage and release gate. | Status review |
| Contributor/byline change | Require documented agreement and reassess acknowledgments/contributions. | Hold/review |
| AI use is disclosed or suspected | Check disclosure, provenance, human review, and confidentiality. | Targeted |
| Pre-release gate | Re-run source-status, disclosure, unresolved-case, and decision-log checks. | Release validation |
| Post-publication update | Preserve the public record and determine whether correction, notice, or other action is needed. | Update review |

## 3. Inputs

### 3.1 Required inputs

- chapter manuscript in an inspectable format;
- chapter metadata and author/contributor list;
- MWM rule registry and approved volume decisions;
- resolved citation/reference graph from Reference & Citation Integrity;
- available source texts, metadata records, and status records;
- quotation and translation markers;
- funding, conflict, ethics, consent, data/code, permissions, and AI-use declarations when applicable;
- prior integrity findings, author responses, and editorial decision log;
- source-access and confidentiality policy;
- chapter profile describing discipline, methods, populations, data, and expected components.

### 3.2 Optional inputs

- source PDFs or archived versions;
- institutional or publisher correspondence;
- contributor statements or CRediT roles;
- prior versions and tracked changes;
- similarity/overlap leads from an approved tool;
- correction, retraction, withdrawal, or expression-of-concern notices;
- external expert or discipline-specific verification.

### 3.3 Protected inputs

Treat the following as protected text or protected records: direct quotations, participant names and sensitive details, author correspondence, institutional allegations, reviewer comments, confidential manuscripts, raw data, personal contact information, and legal/ethics materials. Do not expose them to an unapproved tool or reproduce them beyond the authorized case record.

## 4. Authoritative sources and rule hierarchy

| Tier | Authority | Application |
|---|---|---|
| 1 | MWM project instructions and approved volume decisions | Governs local requirements, scope, release authority, and author-preserving boundaries. |
| 2 | Current MWM decision log, chapter metadata, author declarations, and documented responses | Governs local facts, exceptions, version state, and case closure. |
| 3 | Explicitly delegated APA, discipline, publisher, institutional, ethics, copyright, or permissions policy | Governs specialized requirements only when the delegation is recorded. |
| 4 | COPE, ICMJE, CSE, Crossref, CRediT/NISO, ORI, and COS frameworks | Supplies definitions, process patterns, taxonomies, and evidentiary boundaries. |
| 5 | The primary source cited by the chapter | Governs what the source says, the scope of its claim, and its version/status. |
| 6 | General reference works or model inference | Generates questions only; cannot resolve an integrity case. |

When authorities conflict, record the conflict. Apply the highest applicable tier, preserve the lower-tier source as context, and escalate when the conflict could change a claim, status, contributor record, or release decision.

## 5. Preconditions

Before running a substantive integrity review, the system must verify:

1. the chapter and version are identified;
2. the review stage and trigger are recorded;
3. the governing MWM rules and delegated authorities are available;
4. confidentiality permissions for every tool are known;
5. the citation/reference graph has a status (`complete`, `partial`, or `unresolved`);
6. the source-access log can distinguish local, live, web-only, inaccessible, and author-supplied evidence;
7. every open finding has a case owner or is marked unassigned for routing;
8. the model is prohibited from issuing public allegations or contacting third parties without authorization.

If a precondition fails, return `blocked` or `source_unavailable` with a precise next action. Do not compensate with model confidence.

## 6. Skill map

| Skill ID | Skill | Core question | Default intervention |
|---|---|---|---|
| `CEI-01` | Claim-to-Source Fit | Does the cited source support the claim’s content, scope, certainty, and causal language? | Query or qualify; never silently strengthen/weaken meaning. |
| `CEI-02` | Quotation and Paraphrase Integrity | Does the quoted or paraphrased passage accurately represent the source with appropriate attribution and locator? | Verify, query, or mark source unavailable. |
| `CEI-03` | Source Identity and Status | Is the cited work the intended work, and is its version/status current and accurately represented? | Correct metadata or escalate status. |
| `CEI-04` | Overlap/Plagiarism Signal Review | Is there evidence of unattributed or misleading reuse that warrants human review? | Evidence-backed signal and neutral query; no finding. |
| `CEI-05` | Authorship/Contributorship Signal Review | Are byline, contribution, acknowledgment, and affiliation records coherent and agreed? | Query, hold, or institutional route; no arbitration. |
| `CEI-06` | Disclosure and Transparency Review | Are applicable funding, conflicts, ethics, consent, data, code, registration, and AI statements present and consistent? | Missing/inconsistent disclosure signal. |
| `CEI-07` | Serious Concern Routing | Does an integrity concern require evidence preservation, a release hold, or referral? | Immediate senior/editorial/institutional route. |
| `CEI-08` | Internal Factual Consistency | Do names, dates, numbers, claims, tables, and source statuses contradict each other? | Route meaning-bearing contradictions to the right owner. |
| `CEI-09` | Editorial AI Use and Confidentiality | Was AI use transparent, human-reviewed, attributed where needed, and confidentiality-safe? | Pass, query, or immediate confidentiality escalation. |
| `CEI-10` | Integrity Report and Decision Log | Is each signal actionable, evidenced, owned, and closable? | Release-facing report and gate. |

## 7. Operating principles

### 7.1 Signal before allegation

Use language such as `possible mismatch`, `unverified quotation`, `source-status concern`, `authorship issue requiring agreement`, or `potential overlap requiring review`. Reserve formal terms such as `plagiarism`, `fabrication`, `falsification`, and `misconduct` for quoted authority findings or an authorized human record.

### 7.2 Evidence before action

Every finding must preserve the exact manuscript span, source/record, locator, access status, comparison result, and reason. A model’s intuition is not evidence.

### 7.3 Proportionate remedy

Choose the least consequential action that protects the record while evidence is incomplete: pass, query, qualify, correct, replace source, hold, refer, or block. A central result, contributor record, confidentiality event, or public-status issue receives a higher threshold than a minor attribution or metadata question.

### 7.4 Ownership before closure

An editor may identify and route. The author group owns authorship facts and responses. Institutions own institutional investigations and authorship disputes. Source owners/publishers own source status and corrections. Production owns the final version and metadata. No case closes without an authorized owner and closure evidence.

### 7.5 Preserve disagreement

Store the author’s or source owner’s response as evidence. Do not overwrite the original finding when a response changes the conclusion. Close with a decision record that explains why the evidence was accepted, rejected, or left unresolved.

### 7.6 No-change is a valid result

A source may be retracted but legitimately discussed; a similar phrase may be common or correctly quoted; a historical name may be accurate for its period; and a disclosure may be sufficient. The report must be able to say `no action after review` with evidence.

## 8. Records and schemas

### 8.1 Rule record

```yaml
rule_id: IR-000
skill_id: CEI-00
title: short operational name
authority_tier: 1-6
policy_status: required | recommended | permitted | contextual | delegated
scope: chapter | section | claim | source | contributor | production_record
trigger: intake | targeted | response | status_change | release
detector: deterministic | source_comparison | consistency_graph | human_review
required_inputs: []
evidence_required: []
default_status: verified | signal | source_unavailable | disputed | referred | blocked
intervention: pass | query | qualify | correct | hold | refer | block
owner: skill_or_role
version: 0.1.0
```

### 8.2 Finding record

```yaml
finding_id: SEI-000
skill_id: CEI-00
chapter_id: MWM-000
version_id: v0.0
stage: intake | review | response | production | release | post_publication
status: verified | supported_with_scope | signal | source_unavailable | disputed | referred | resolved | blocked
risk_level: low | moderate | high | critical
exact_text: manuscript span or protected locator
location: page/paragraph/section/asset/claim id
claim_or_object: claim | quote | paraphrase | source | contributor | disclosure | entity | status | AI_event
source_or_record: source id, DOI, URL, notice, or internal record
source_access_status: local | live | web_only | author_supplied | inaccessible | stale | unknown
comparison_or_basis: concise evidence summary
authority: rule/source/decision id
reason: observable explanation without intent inference
owner: role/person/team
next_action: precise action and due stage
confidence: high | medium | low
escalation: none | editor | senior_editor | author_group | institution | publisher | legal_or_ethics | security
response: null or dated response record
closure_condition: testable condition
created_at: ISO-8601
updated_at: ISO-8601
```

### 8.3 Decision record

```yaml
decision_id: DEC-000
finding_ids: []
decision: pass | query | qualify | correct | replace_source | hold | refer | notice | block
decision_owner: role/person
authority: rule or approved decision
evidence_considered: []
response_summary: concise and neutral
rationale: why the remedy is proportionate
release_effect: none | track | hold | block
approved_at: ISO-8601
supersedes: null
```

## 9. Procedure

### Step 1 — Initialize

Record chapter ID, version, stage, trigger, governing policy versions, tools, model, confidentiality status, and assigned owner.

### Step 2 — Build the integrity inventory

Parse claims, citations, quotations, paraphrases, names, organizations, dates, numbers, tables, contributor records, disclosures, methodological claims, AI-use declarations, and source-status fields. Assign stable object IDs so findings refer to objects rather than unstable line positions.

### Step 3 — Protect and classify content

Mark quotations, participant details, confidential correspondence, reviewer material, and sensitive records. Route protected content only through approved tools. Classify each check as deterministic, source-comparison, graph-consistency, or human review.

### Step 4 — Run deterministic checks

Check citation/reference identity, repeated source variants, missing quotation locators, missing declarations required by local policy, byline/contribution field mismatches, version/status fields, and internal contradictions that can be established from the supplied record.

### Step 5 — Run source-comparison checks

For each material claim or quotation, compare the manuscript with the source text or verified metadata. Record scope, certainty, modality, causality, attribution, and version. If the source cannot be accessed, return `source_unavailable` rather than guessing.

### Step 6 — Run integrity-signal checks

Review overlap leads, authorship changes, disclosure inconsistencies, ethics/consent omissions, AI-use events, suspicious source/status patterns, and allegations. Ask for evidence and route according to ownership. Do not escalate from a model score alone.

### Step 7 — Evaluate risk and intervention

Assess centrality, potential effect on interpretation or credit, public/reputational/legal/ethical risk, evidence quality, and reversibility. Choose the proportionate action and assign an owner.

### Step 8 — Reassess responses

Compare the response with the original evidence. If resolved, create a decision record. If disputed or incomplete, preserve the case and route. Do not silently delete the initial finding.

### Step 9 — Run release gate

Confirm no unresolved `high`/`critical` case, source-unavailable central quotation, disputed authorship change, confidentiality incident, stale/retracted central source, missing mandatory disclosure, or unapproved public-status action remains open.

## 10. CEI-01 — Claim-to-Source Fit

### Purpose

Determine whether the cited source supports the claim as written, including scope, certainty, population, date, direction, causality, and limitations.

### Detection logic

1. Segment the sentence or paragraph into atomic claims.
2. Identify the citation(s) attached to each claim.
3. Retrieve the relevant source passage, abstract, metadata, or verified record.
4. Compare subject, predicate, population, method, result, qualifier, and time frame.
5. Compare modality (`may`, `suggests`, `is associated with`, `causes`, `proves`) and scope.
6. Classify as `verified`, `supported_with_scope`, `signal`, or `source_unavailable`.
7. Recommend qualification, added citation, source replacement, or author query; never silently rewrite a meaning-bearing claim.

### High-risk conditions

- causal language where the source reports association;
- universal language where the source is limited to a sample or context;
- certainty that removes a source’s qualification;
- a claim materially central to the chapter’s conclusion;
- source status or version changed after the claim was drafted.

## 11. CEI-02 — Quotation and Paraphrase Integrity

### Detection logic

- Match quoted text character-for-character where the source is available, allowing only approved typographic differences.
- Verify omissions, insertions, brackets, ellipses, translation labels, and locators.
- Compare paraphrase meaning and attribution, not only shared words.
- Identify qualifier loss, speaker/source substitution, altered negation, changed population, and changed date.
- Distinguish `source_unavailable` from `mismatch`.
- For translated material, record original source, translator/translation status, and whether the local policy permits the treatment.

### Intervention

Minor formatting discrepancy: query or correct with evidence. Meaning-changing mismatch: high-risk human review. Unavailable source: do not certify; request a source copy, author attestation, or replacement/qualification. Never invent a locator.

## 12. CEI-03 — Source Identity and Status

### Detection logic

- Match author, title, year, edition/version, DOI/URL, and cited object to the reference record.
- Detect one work represented by multiple variants or multiple works collapsed into one record.
- Query Crossref, publisher, repository, or other approved status source at a date-stamped point in time.
- Identify correction, retraction, withdrawal, expression-of-concern, preprint, new version, or supersession signals.
- Record whether the source is central, incidental, or being discussed as an object.

### Intervention

Metadata mismatch routes to Reference & Citation Integrity. A status change affecting interpretation or credit routes to senior editorial review. A retracted source may be retained when explicitly discussed, but its status and role must be visible. Do not treat Crossmark or any status badge as a guarantee of validity.

## 13. CEI-04 — Overlap/Plagiarism Signal Review

### Detection logic

1. Accept a similarity lead only from an approved tool or documented comparison.
2. Obtain the suspected source and preserve exact overlapping spans.
3. Determine whether the overlap is quotation, paraphrase, common language, methods language, translation, author’s prior work, or unattributed reuse.
4. Assess extent, location, data/idea reuse, attribution, and whether the source was presented as the author’s own.
5. Contact the author neutrally for explanation and preserve the response.
6. Route unresolved or material cases to the integrity lead, institution, or publisher according to policy.

### Prohibited inference

The Skill must not infer plagiarism, intent, or deception from a percentage, writing style, language proficiency, or model-generated suspicion. The output is an evidence-backed overlap concern or a no-action result.

## 14. CEI-05 — Authorship/Contributorship Signal Review

### Detection logic

- Compare byline, contributor statement, acknowledgments, affiliations, correspondence, and author declarations.
- Check that required authorship criteria or local MWM criteria are addressed by the author group.
- If CRediT is used, compare roles for internal coherence; do not treat a role as proof of authorship or non-authorship.
- For an addition/removal/order change, require reason, all-author agreement, and written agreement from a removed/added person where policy requires.
- If agreement is absent, hold the change and refer to the relevant institution or governing owner.

### Prohibited inference

The editor/model may not decide author entitlement, author order, ghost/guest/gift authorship, or whether a contributor deserves authorship. It may identify a mismatch or missing agreement and route it.

## 15. CEI-06 — Disclosure and Transparency Review

### Detection logic

- Load the chapter’s applicable disclosure matrix from the MWM rule registry.
- Check presence and consistency of funding, competing interests, ethics approval, consent, data/code/materials availability, registration/protocol, permissions, and AI-use statements when relevant.
- Compare declarations across cover materials, chapter text, acknowledgments, contributor records, and author responses.
- Apply TOP-like checks only when the chapter makes relevant empirical or methodological claims and the local policy delegates them.
- Classify `missing`, `inconsistent`, `not applicable with rationale`, or `complete`.

### Prohibited inference

An omitted declaration is a query or signal, not proof that a conflict, consent failure, or ethical breach occurred. An employer, funder, topic, or relationship is not itself evidence of improper influence.

## 16. CEI-07 — Serious Concern Routing

### Trigger conditions

- possible fabrication/falsification or materially unreliable data;
- source evidence indicates a central claim may be invalid;
- unresolved or disputed authorship likely to affect release;
- confidentiality breach involving a manuscript or sensitive material;
- high-risk allegation involving a person, institution, participant, or legal claim;
- a correction/retraction/status issue that could materially affect interpretation or credit.

### Procedure

1. Freeze routine edits to the affected material.
2. Preserve evidence and access permissions.
3. Notify the designated senior editorial/integrity owner.
4. Use neutral, allegation-safe language.
5. Identify the correct author-group, institution, funder, publisher, legal, ethics, or security route.
6. Record whether release is held and what evidence is required.
7. Do not investigate beyond authorized scope.

## 17. CEI-08 — Internal Factual Consistency

### Detection logic

Build a lightweight entity/claim graph for names, organizations, dates, numbers, sample sizes, populations, methods, tables, figures, and source status. Flag incompatible values when they refer to the same object and cannot be explained by time, version, subgroup, or historical context.

Examples include a table total that conflicts with prose, an organization name inconsistent with the date, a sample size that changes between methods and results, or a source described as published when the record is a preprint.

Route meaning-bearing contradictions to the relevant technical, statistical, source, or integrity owner. Do not silently pick the more plausible value.

## 18. CEI-09 — Editorial AI Use and Confidentiality

### Required record

- tool or model name and version;
- date and purpose of use;
- manuscript material processed;
- authorization and confidentiality status;
- whether generated content was accepted, edited, or rejected;
- human reviewer responsible for accuracy, attribution, and originality;
- disclosure language required by MWM policy.

### Detection logic

Check for an applicable AI-use declaration, unverified citations, generated quotations, missing attribution, source-free factual claims, and evidence that a confidential manuscript was uploaded to an unapproved system.

An unauthorized confidentiality event is `critical` and escalates immediately to the designated senior/security owner. Do not continue ordinary processing as if no incident occurred.

## 19. CEI-10 — Integrity Report and Decision Log

The report must include:

1. review metadata and scope;
2. source/access limitations;
3. summary of open, resolved, and blocked findings;
4. finding table with exact text, evidence, source, status, confidence, owner, and next action;
5. author/source/institution responses;
6. decisions and rationale;
7. release effect and unresolved-risk statement;
8. next review trigger and version lineage.

### Suggested report table

| ID | Skill | Location | Signal/status | Evidence | Owner | Action | Confidence | Release effect |
|---|---|---|---|---|---|---|---|---|
| SEI-000 | CEI-00 | section/claim | signal | source + locator + access | role | query/hold/refer | high/medium/low | track/hold/block |

## 20. Intervention thresholds

| Threshold | Use | Examples |
|---|---|---|
| `AUTO_RECORD` | Record a deterministic fact without changing text. | Citation variant, missing field, status lookup date. |
| `PASS` | Evidence supports the object or no issue remains after review. | Correctly attributed quotation; historical name verified. |
| `QUERY` | Plausible issue with low/moderate risk and a clear author/source question. | Missing locator, scope overstatement, inconsistent declaration. |
| `QUALIFY` | Claim or source can remain only with explicit scope/status language approved by the owner. | Retracted source discussed as historical object; association not causation. |
| `CORRECT` | Deterministic error can be repaired without changing intended meaning and the owner approves. | DOI typo, reference identity, correction notice metadata. |
| `HOLD` | Evidence or agreement is required before release. | Disputed authorship, central source status, material quotation mismatch. |
| `REFER` | Matter belongs to an institution, source owner, publisher, funder, legal/ethics, or security owner. | Misconduct allegation, authorship dispute, confidentiality incident. |
| `BLOCK` | Required authority, evidence, or closure is absent and release would create material risk. | Unresolved critical case or source-unavailable central quotation. |

## 21. Evidence requirements

### Minimum evidence by finding type

| Finding | Minimum evidence |
|---|---|
| Claim/source fit | Claim span, citation, source passage/metadata, scope comparison, source access status. |
| Quotation | Exact quote, source text or access attempt, locator, mismatch/confirmation details. |
| Overlap | Both text spans, source identity, extent/context, attribution state, response or evidence request. |
| Authorship | Byline, contribution/acknowledgment records, request, all-author response, institutional route if needed. |
| Disclosure | Applicable local requirement, fields checked, declarations compared, author query/response. |
| Source status | DOI/URL, status source, query date, notice/version, effect on chapter use. |
| Misconduct signal | Exact allegation/evidence, provenance, confidentiality status, authorized owner, referral path. |
| AI event | Tool, purpose, material processed, permission, disclosure, human review, incident record if applicable. |

### Access-status rule

`web_only`, `inaccessible`, and `unknown` are evidence states, not minor administrative notes. A source-unavailable result cannot be promoted to verified because the claim appears plausible.

## 22. Confidence

Confidence describes the Skill’s confidence in the classification, not the truth of the allegation.

| Confidence | Meaning | Required treatment |
|---|---|---|
| High | Deterministic mismatch or direct source comparison is clear, with strong authority and complete evidence. | May recommend correction/query; human approves meaning/status changes. |
| Medium | Evidence is credible but scope, context, or source access is incomplete. | Query or refer; do not close as verified. |
| Low | Signal depends on model inference, similarity, missing context, or unverified source. | Signal only; evidence request; no release-blocking allegation without human review. |

## 23. Human-escalation rules

Escalate when:

- the issue could accuse a person or institution of misconduct, plagiarism, fraud, or unethical conduct;
- authorship, contribution, order, or affiliation is disputed;
- a central result or recommendation may be invalid;
- a source is retracted, corrected, withdrawn, or superseded in a way that affects interpretation;
- consent, human-subjects, sensitive-data, or privacy questions arise;
- a living person or organization is the subject of an unsupported harmful claim;
- the source is unavailable but the quotation/claim is central;
- external AI processing may have breached confidentiality;
- the remedy could be a public correction, expression of concern, withdrawal, retraction, or legal notice;
- applicable authorities conflict;
- the model cannot state what evidence would close the issue.

## 24. Tool and model routing

| Task | Preferred route | Human checkpoint |
|---|---|---|
| Parse claims, citations, names, and declarations | Deterministic parser + constrained model | Sampling QA |
| Compare quotation/claim to source | Source-retrieval tool + comparison model | Editor confirms scope and wording |
| Verify DOI/metadata/status | Reference tool/Crossref/publisher record | Date-stamped status review |
| Detect overlap lead | Approved similarity tool or document comparison | Integrity editor reviews context |
| Assess contributor mismatch | Structured form comparison | Author group/institution owns dispute |
| Evaluate disclosure completeness | Rule registry + checklist | Volume owner confirms applicability |
| Handle serious concern | Restricted evidence workflow | Senior integrity/editorial owner |
| Handle confidential AI event | Approved internal process | Security/privacy owner |
| Produce report | Structured report generator | Editor signs decision record |

Do not use a general external model for confidential manuscript content unless the project has explicitly approved that tool and data path.

## 25. QA tests

### 25.1 Automated tests

- every finding has a valid skill ID, status, risk level, owner, next action, and closure condition;
- no formal misconduct label appears without an imported authorized determination;
- `source_unavailable` findings cannot be emitted as `verified` without new evidence;
- authorship-dispute fixtures route to author group/institution and do not produce author-order decisions;
- status records include query date and source locator;
- correction, expression-of-concern, retraction, withdrawal, and preprint statuses remain distinct;
- confidential-material paths reject unapproved external tools;
- every `high`/`critical` finding has an escalation owner;
- decision records preserve superseded findings and responses;
- Markdown and Word headings match exactly.

### 25.2 Human QA

- sample no-action cases for false positives;
- review all high/critical cases;
- verify that the wording is allegation-safe;
- check that source comparisons preserve qualifiers and modality;
- confirm that corrections and notices are proportionate;
- confirm that local MWM policy—not external exemplar policy—controls release.

### 25.3 Evaluation set

Run `04_Evaluation_Set/evaluation_set.md` with at least 36 fixtures. Minimum pass conditions are: no unsupported formal finding, source-unavailable cases remain uncertified, authorship disputes are not arbitrated, status remedies are not conflated, and confidentiality incidents escalate.

## 26. Failure modes and mitigations

| Failure | Mitigation |
|---|---|
| Citation presence treated as source support | Require source-text/scope comparison. |
| Similarity percentage treated as plagiarism | Use overlap lead only; preserve context and attribution. |
| Model infers intent from tone or style | Ban intent inference; use allegation-safe language. |
| Author affiliation treated as conflict | Require policy applicability and disclosure evidence. |
| Authorship issue adjudicated by editor/model | Hold, document, and refer. |
| Retracted source automatically deleted | Classify role; permit explicit discussion with status. |
| Correction escalated to retraction | Apply impact/evidence taxonomy and senior approval. |
| Source unavailable treated as verified | Enforce access-status state. |
| Historical name treated as error | Check date/context and source identity. |
| AI-generated citation accepted because it looks real | Verify metadata/source; do not rely on plausibility. |
| Confidential manuscript uploaded externally | Approved-tool gate and immediate incident escalation. |
| Open case lost when a new version is created | Preserve version lineage and decision history. |

## 27. Examples

### 27.1 Claim scope

**Manuscript:** “The study proved that the intervention causes improved attendance.”  
**Source:** Reports an association in one observational sample and notes limits.  
**Output:** `CEI-01`, `supported_with_scope`, high confidence; cite source passage; query causal language; owner author/editor; do not silently replace “proved.”

### 27.2 Quotation qualifier

**Manuscript:** A quotation omits “in this sample” from the source.  
**Output:** `CEI-02`, `signal`, high risk if central; preserve both spans and locator; hold affected claim pending author/source review.

### 27.3 Legitimate retracted-source discussion

**Manuscript:** “The retraction illustrates how peer-review failures can propagate.”  
**Output:** `CEI-03`, pass with status framing if the retraction is accurately documented; do not remove the source merely because it is retracted.

### 27.4 Authorship dispute

**Request:** Add a contributor after submission; one existing author objects.  
**Output:** `CEI-05`, `disputed`, hold byline change; request all-author agreement and refer to institution if unresolved; never decide entitlement.

### 27.5 Missing disclosure

**Manuscript:** Funding statement present; local policy requires a conflicts statement; none appears.  
**Output:** `CEI-06`, `signal`, query the author; do not infer a conflict.

### 27.6 AI confidentiality event

**Event:** A reviewer uploads an unpublished chapter to an external model without permission.  
**Output:** `CEI-09`, `critical`, immediate security/senior escalation and evidence preservation; stop routine processing.

## 28. Counterexamples

- Do not label a paragraph plagiarism because an eight-word phrase matches a common definition.
- Do not label a citation fabricated because a DOI has a typo; route it to metadata verification.
- Do not label a source unreliable because it is a preprint; label its status and check whether the manuscript represents it accurately.
- Do not label an employer or funder a conflict without a disclosure policy and evidence.
- Do not call an authorship disagreement misconduct unless an authorized record establishes a separate issue.
- Do not force a current organization name into a historical account when the historical name is accurate for the period.
- Do not treat a retracted source as unusable when the chapter explicitly analyzes the retraction.
- Do not upgrade a web-only source to verified when the quoted passage was never inspected.
- Do not classify an author’s honest correction as evidence of unreliability or bad faith.
- Do not fix a central numerical contradiction by selecting the most plausible number.

## 29. Evaluation set and acceptance criteria

The evaluation set is versioned at `MWM-SEI-EVAL-0.1` and contains 36 fixtures covering claim fit, quotations, source status, overlap, authorship, disclosures, ethics, AI, contradictions, and serious concerns.

Acceptance requires:

1. zero unsupported formal misconduct findings;
2. 100% preservation of source-unavailable status until evidence arrives;
3. 100% non-arbitration of authorship disputes;
4. 100% escalation of confidentiality incidents;
5. correct distinction among correction, expression of concern, retraction, withdrawal, and no action in the status fixtures;
6. evidence fields complete for every high/critical finding;
7. human reviewers judge the report’s language fair, neutral, and actionable;
8. no material meaning change introduced by an automatic intervention.

## 30. Versioning and governance

Version the specification, rule registry, source manifest, evaluation set, and decision-log schema together when a change affects behavior. A change requires:

- change ID and rationale;
- affected rule/skill IDs;
- authority/source change;
- before/after examples;
- updated counterexamples and evaluation fixtures;
- regression results;
- owner approval;
- effective date and superseded version.

Retain source snapshots or access records for every release-affecting decision. Re-run status checks at release because source correction/retraction status can change.

## 31. Release checklist

- [ ] Chapter and version identified.
- [ ] MWM rule/decision versions recorded.
- [ ] Citation/reference graph status known.
- [ ] All central claims and quotations have source/locator evidence or an explicit source-unavailable status.
- [ ] Retraction/correction/status checks are date-stamped.
- [ ] No unresolved high/critical source or claim issue remains.
- [ ] Authorship/byline/contributor changes have documented agreement or an approved route.
- [ ] Required funding, conflict, ethics, consent, data, permissions, and AI disclosures are complete or explicitly not applicable.
- [ ] No unapproved confidential AI processing occurred.
- [ ] All serious concerns have an owner, next action, and closure condition.
- [ ] Decision log preserves responses and superseded findings.
- [ ] Technical, copyediting, reference, completeness, and production handoffs are complete.
- [ ] Senior editorial owner signs the release decision.

## 32. Open decisions for MWM

1. Approve the volume-level disclosure matrix.
2. Define the MWM material-risk threshold and mandatory hold classes.
3. Name the editorial integrity lead and institutional/publisher referral route.
4. Decide whether CRediT is required, optional, or used only for flagged cases.
5. Approve source-status services and release-time lookup procedure.
6. Define treatment of preprints, retracted sources, translations, and overlapping publications in MWM chapters.
7. Approve AI tools, confidentiality rules, and disclosure language.
8. Define the evidence-retention period and access controls for integrity case records.
9. Approve remedy language for correction, expression of concern, withdrawal, and retraction of chapter/volume content.

## 33. Research basis and limitations

The design is grounded in the local corpus at `05_Scholarly_Editorial_Integrity`, including supplied MWM/AISL/APA exemplars; COPE’s Core Practices, flowcharts, cooperation guidance, authorship discussion, and retraction guidance; ICMJE recommendations; ORI/42 CFR Part 93; CRediT/NISO; Crossref Crossmark; CSE recommendations; and COS TOP 2025.

The strongest shared finding is architectural: mature systems separate signal detection, evidence capture, ownership, remedy/status, and record update. No source supports a universal text-only plagiarism threshold, authorship adjudication by editors, or inference of intent from prose. This specification therefore treats integrity review as an auditable, evidence-first routing capability.

Some COPE and Crossref sources were web-accessed but blocked for local automated retrieval. Their canonical URLs and access limitations are recorded in the corpus manifest and access log. Before a source is used as controlling authority for a live case, an editor should verify the current source and local policy.
