# Decisions carried into the University Press Workbench

This design was checked against the Codex tasks from the week before September 9, 2026 that dealt with standing up University Press capacity.

## Ownership and operating model

`Not sure. Navy Workbench` and `Revise LunaRoute assignment memo` settled the main division of responsibility. University Press owns the professional constitution and the right to accept or reject editorial work. Navy Yard Workbench Foundry designs, maintains, and runs the machinery. The software therefore compiles a new policy-bound plan for every batch instead of letting a worker choose its own rules.

The same work established the need for bidirectional receipts: every proposal must reconcile to a source manifest, while unresolved cases and later human decisions need to flow back into future policy work. This release writes an append-only observation stream but leaves acceptance to the press.

## LunaRoute lane choice

`LunaRoute Lane Routing` established an urgency-first rule. Foreground lanes are for work with an immediate deadline; ordinary volume processing belongs in background lanes. The workbench therefore defaults to `glm-5.3-background`, permits no more than six parallel chapters, and keeps the foreground model as an explicit choice.

`Admiral Luna Route & Gemini Coordination` named University Press stand-up as active work and confirmed the GLM 5.3 route used here. A separate credential-configuration task showed that a LunaRoute credential may have appeared in prior task history. Rotate that credential before real unpublished manuscripts are processed.

## Resulting design choices

The prior work is visible in five concrete controls: immutable per-run plans, source hashes before every external stage, RCI before SEI, evidence and uncertainty retained with each proposal, and no code path for accepting an edit or authorizing publication.
