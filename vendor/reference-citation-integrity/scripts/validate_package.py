#!/usr/bin/env python3
"""Validate the RCI package structure, JSON assets, schemas, examples, and eval coverage."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "01_SPECIFICATION.md",
    "SKILL.md",
    "agents/openai.yaml",
    "02_RULES/ruleset.json",
    "02_RULES/decision_hooks.json",
    "02_RULES/source_taxonomy.json",
    "02_RULES/authority_registry.json",
    "schemas/run-manifest.schema.json",
    "schemas/citation-record.schema.json",
    "schemas/reference-record.schema.json",
    "schemas/finding.schema.json",
    "schemas/source-record.schema.json",
    "schemas/ledger-entry.schema.json",
    "schemas/decision-record.schema.json",
    "schemas/run-result.schema.json",
    "schemas/cross-family-contracts.json",
    "evals/fixture_catalog.json",
    "evals/rule_fixture_crosswalk.json",
    "evals/adversarial_negative_controls.json",
    "evals/integration_cases.json",
    "evals/scorer.py",
    "CHANGELOG_REGRESSION/CHANGELOG.md",
    "CHANGELOG_REGRESSION/regression-intake.schema.json",
    "CHANGELOG_REGRESSION/production-failure.schema.json",
    "CHANGELOG_REGRESSION/regression_policy.json",
]


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_with_jsonschema(errors: list[str], schema_path: Path, instance_path: Path) -> str:
    try:
        import jsonschema  # type: ignore
        from referencing import Registry, Resource  # type: ignore
    except ImportError:
        return "jsonschema-unavailable"
    try:
        schema = load(schema_path)
        instance = load(instance_path)
        resources = {}
        for candidate in (ROOT / "schemas").glob("*.schema.json"):
            candidate_schema = load(candidate)
            if "$id" in candidate_schema:
                resources[candidate_schema["$id"]] = Resource.from_contents(candidate_schema)
        registry = Registry().with_resources(resources.items())
        jsonschema.Draft202012Validator(schema, registry=registry, format_checker=jsonschema.FormatChecker()).validate(instance)
    except Exception as exc:  # validator reports precise path in the exception
        add(errors, f"{instance_path.relative_to(ROOT)} against {schema_path.relative_to(ROOT)}: {exc}")
    return "jsonschema-validated"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    statuses: list[str] = []

    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file():
            add(errors, f"missing required file: {relative}")

    skill = ROOT / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            add(errors, "SKILL.md lacks valid frontmatter delimiters")
        else:
            frontmatter = text.split("\n---\n", 1)[0][4:]
            keys = [line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if ":" in line and not line.startswith(" ")]
            if keys != ["name", "description"]:
                add(errors, f"SKILL.md frontmatter keys must be name, description; found {keys}")
            if "name: reference-citation-integrity" not in frontmatter:
                add(errors, "SKILL.md name does not match folder")
            if "description:" not in frontmatter or len(frontmatter.split("description:", 1)[1].strip()) < 25:
                add(errors, "SKILL.md description is missing or too short")
        if "TODO" in text or "TBD" in text:
            add(errors, "SKILL.md contains TODO/TBD placeholder")

    yaml = ROOT / "agents/openai.yaml"
    if yaml.is_file():
        yaml_text = yaml.read_text(encoding="utf-8")
        for required in ("display_name:", "short_description:", "default_prompt:"):
            if required not in yaml_text:
                add(errors, f"agents/openai.yaml missing {required}")
        if "$reference-citation-integrity" not in yaml_text:
            add(errors, "agents/openai.yaml default_prompt does not mention $reference-citation-integrity")

    json_paths = sorted(ROOT.rglob("*.json"))
    loaded: dict[Path, Any] = {}
    for path in json_paths:
        try:
            loaded[path] = load(path)
        except json.JSONDecodeError as exc:
            add(errors, f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    rules_path = ROOT / "02_RULES/ruleset.json"
    addenda_path = ROOT / "02_RULES/ruleset_addenda.json"
    rule_ids: set[str] = set()
    if rules_path in loaded:
        rules = loaded[rules_path]
        for rule in rules.get("rules", []):
            rule_id = rule.get("id")
            if not rule_id or rule_id in rule_ids:
                add(errors, f"duplicate or missing base rule ID: {rule_id}")
            rule_ids.add(rule_id)
    if addenda_path in loaded:
        for rule in loaded[addenda_path].get("rules", []):
            rule_id = rule.get("id")
            if not rule_id or rule_id in rule_ids:
                add(errors, f"duplicate or missing addendum rule ID: {rule_id}")
            rule_ids.add(rule_id)

    catalog_path = ROOT / "evals/fixture_catalog.json"
    catalog = loaded.get(catalog_path)
    if catalog:
        fixtures = catalog.get("fixtures", [])
        ids = [fixture.get("fixture_id") for fixture in fixtures]
        if len(ids) != len(set(ids)):
            add(errors, "fixture IDs are not unique")
        expected_counts = catalog.get("fixture_counts", {})
        actual_counts: dict[str, int] = {}
        for fixture in fixtures:
            actual_counts[fixture.get("kind")] = actual_counts.get(fixture.get("kind"), 0) + 1
            if fixture.get("synthetic") is not True:
                add(errors, f"{fixture.get('fixture_id')}: synthetic must be true")
            for rule_id in fixture.get("gold", {}).get("expected_rule_ids", []) + fixture.get("gold", {}).get("must_not_emit_rule_ids", []):
                if rule_id not in rule_ids:
                    add(errors, f"{fixture.get('fixture_id')}: unknown gold rule {rule_id}")
        for kind, expected in expected_counts.items():
            if actual_counts.get(kind, 0) != expected:
                add(errors, f"fixture count {kind}: expected {expected}, found {actual_counts.get(kind, 0)}")

        fixture_schema = ROOT / "evals/fixture_contract.schema.json"
        if fixture_schema.is_file():
            for fixture in fixtures:
                temp = ROOT / "evals" / f".validate-{fixture['fixture_id']}.json"
                # Validate in memory when jsonschema is available to avoid creating package files.
                try:
                    import jsonschema  # type: ignore
                    schema = load(fixture_schema)
                    jsonschema.Draft202012Validator(schema).validate(fixture)
                except ImportError:
                    statuses.append("jsonschema-unavailable")
                except Exception as exc:
                    add(errors, f"fixture {fixture['fixture_id']} contract invalid: {exc}")

    crosswalk_path = ROOT / "evals/rule_fixture_crosswalk.json"
    crosswalk = loaded.get(crosswalk_path)
    if crosswalk and catalog:
        crosswalk_rule_ids: set[str] = set()
        known_fixture_ids = {fixture["fixture_id"] for fixture in catalog["fixtures"]}
        for row in crosswalk.get("rows", []):
            rule_id = row.get("rule_id")
            crosswalk_rule_ids.add(rule_id)
            if rule_id not in rule_ids:
                add(errors, f"crosswalk unknown rule {rule_id}")
            seen: set[str] = set()
            for category in ("positive", "negative", "adversarial", "integration"):
                if not row.get(category):
                    add(errors, f"crosswalk {rule_id} missing {category} coverage")
                for fixture_id in row.get(category, []):
                    if fixture_id not in known_fixture_ids:
                        add(errors, f"crosswalk {rule_id} references unknown fixture {fixture_id}")
                    if fixture_id in seen:
                        add(errors, f"crosswalk {rule_id} repeats fixture {fixture_id} across categories")
                    seen.add(fixture_id)
        missing = sorted(rule_ids - crosswalk_rule_ids)
        if missing:
            add(errors, f"rules missing from crosswalk: {missing}")

    # Validate every representative schema example against its named schema.
    example_pairs = {
        "run-manifest.example.json": "run-manifest.schema.json",
        "citation-record.example.json": "citation-record.schema.json",
        "reference-record.example.json": "reference-record.schema.json",
        "finding.example.json": "finding.schema.json",
        "source-record.example.json": "source-record.schema.json",
        "ledger-entry.example.json": "ledger-entry.schema.json",
        "decision-record.example.json": "decision-record.schema.json",
        "run-result.example.json": "run-result.schema.json",
    }
    for example_name, schema_name in example_pairs.items():
        example = ROOT / "schemas/examples" / example_name
        schema = ROOT / "schemas" / schema_name
        if example.is_file() and schema.is_file():
            status = validate_with_jsonschema(errors, schema, example)
            statuses.append(status)
            if status == "jsonschema-unavailable":
                warnings.append("jsonschema is unavailable; example validation was limited to JSON syntax")

    # Validate regression schemas against their templates when possible.
    for schema_name, example_name in (("regression-intake.schema.json", "regression-intake.template.json"), ("production-failure.schema.json", "production-failure.template.json")):
        schema = ROOT / "CHANGELOG_REGRESSION" / schema_name
        example = ROOT / "CHANGELOG_REGRESSION" / example_name
        if schema.is_file() and example.is_file():
            status = validate_with_jsonschema(errors, schema, example)
            statuses.append(status)
            if status == "jsonschema-unavailable":
                warnings.append("jsonschema is unavailable; regression template validation was limited to JSON syntax")

    # Cheap static checks that guard the high-risk boundaries even without third-party validators.
    spec = ROOT / "01_SPECIFICATION.md"
    if spec.is_file():
        spec_text = spec.read_text(encoding="utf-8")
        for phrase in ("Do not invent metadata", "Preserve related works", "Human-escalation rules", "Open decisions for editorial adjudication"):
            if phrase not in spec_text:
                add(errors, f"governing specification missing expected boundary phrase: {phrase}")
    skill_text = skill.read_text(encoding="utf-8") if skill.is_file() else ""
    for phrase in ("never invent", "claim support", "silently substitute", "release status"):
        if phrase.lower() not in skill_text.lower():
            add(errors, f"SKILL.md missing boundary phrase: {phrase}")

    result = {"package": "reference-citation-integrity", "pass": not errors, "errors": errors, "warnings": sorted(set(warnings)), "validation_statuses": statuses, "rule_count": len(rule_ids), "json_file_count": len(json_paths)}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())



