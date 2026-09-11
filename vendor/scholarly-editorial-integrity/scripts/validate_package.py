#!/usr/bin/env python3
"""Run structural and schema QA for the Scholarly/Editorial Integrity package."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SPEC_SHA256 = "79E5A4FE73DFDD1422362F161BC9323BF02A7A52F8F3B82FA9267E72D8F48AD0"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    """Hash governed text canonically so a Windows checkout stays verifiable."""
    content = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest().upper()


def validate_instance(instance: Any, schema: dict[str, Any], registry: Any) -> list[str]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover
        return [f"jsonschema unavailable: {exc}"]
    validator = Draft202012Validator(schema, registry=registry)
    return [f"{'.'.join(str(part) for part in error.absolute_path)}: {error.message}" for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    required_files = [
        "01_SPECIFICATION.md","SKILL.md","agents/openai.yaml",
        "02_RULES/ruleset.json","02_RULES/decision_hooks.json","02_RULES/authority_registry.json","02_RULES/protected_records.json",
        "evals/fixture_contract.schema.json","evals/fixture_catalog.json","evals/rule_fixture_crosswalk.json","evals/adversarial_negative_controls.json","evals/integration_cases.json","evals/scorer.py",
        "CHANGELOG_REGRESSION/CHANGELOG.md","CHANGELOG_REGRESSION/regression-intake.schema.json","CHANGELOG_REGRESSION/regression-intake.template.json","CHANGELOG_REGRESSION/production-failure.schema.json","CHANGELOG_REGRESSION/production-failure.template.json","CHANGELOG_REGRESSION/regression_policy.json",
        "scripts/validate_package.py","package_manifest.json"
    ]
    required_files.extend(f"schemas/{name}" for name in ["run-manifest.schema.json","source-access-record.schema.json","claim-record.schema.json","finding.schema.json","decision-record.schema.json","disclosure-record.schema.json","contributor-record.schema.json","ai-event-record.schema.json","finding-ledger.schema.json","run-result.schema.json","cross-family-contracts.json"])
    required_files.extend(f"schemas/examples/{name}" for name in ["run-manifest.example.json","source-access-record.example.json","claim-record.example.json","finding.example.json","decision-record.example.json","disclosure-record.example.json","contributor-record.example.json","ai-event-record.example.json","finding-ledger.example.json","run-result.example.json"])
    for relative in required_files:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    spec_path = ROOT / "01_SPECIFICATION.md"
    if spec_path.is_file() and sha256(spec_path) != EXPECTED_SPEC_SHA256:
        errors.append(f"governing specification hash mismatch: {sha256(spec_path)}")
    skill_path = ROOT / "SKILL.md"
    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        if len(text.splitlines()) > 500:
            errors.append("SKILL.md exceeds the 500-line limit")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append("SKILL.md is missing required frontmatter")
        if re.search(r"\b(TODO|TBD|FIXME)\b", text, re.IGNORECASE):
            errors.append("SKILL.md contains unresolved placeholders")
        if "$scholarly-editorial-integrity" not in text:
            warnings.append("SKILL.md has no explicit invocation example")
    yaml_path = ROOT / "agents/openai.yaml"
    if yaml_path.is_file():
        yaml = yaml_path.read_text(encoding="utf-8")
        for marker in ["interface:","display_name:","short_description:","default_prompt:","policy:","allow_implicit_invocation:"]:
            if marker not in yaml:
                errors.append(f"agents/openai.yaml missing {marker}")
        if "$scholarly-editorial-integrity" not in yaml:
            errors.append("agents/openai.yaml default_prompt must name the skill")

    documents: dict[Path, dict[str, Any]] = {}
    for path in sorted(ROOT.rglob("*.json")):
        try:
            documents[path] = read_json(path)
        except Exception as exc:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    try:
        from referencing import Registry, Resource
    except ImportError as exc:  # pragma: no cover
        errors.append(f"referencing unavailable: {exc}")
        Registry = None
        Resource = None
    registry = None
    if Registry is not None and Resource is not None:
        registry = Registry()
        for document in documents.values():
            if "$id" in document:
                try:
                    registry = registry.with_resource(document["$id"], Resource.from_contents(document))
                except Exception as exc:
                    errors.append(f"cannot register {document.get('$id')}: {exc}")
    schema_map = {path.name: document for path, document in documents.items() if path.name.endswith(".schema.json")}
    if registry is not None:
        examples = {"run-manifest.example.json":"run-manifest.schema.json","source-access-record.example.json":"source-access-record.schema.json","claim-record.example.json":"claim-record.schema.json","finding.example.json":"finding.schema.json","decision-record.example.json":"decision-record.schema.json","disclosure-record.example.json":"disclosure-record.schema.json","contributor-record.example.json":"contributor-record.schema.json","ai-event-record.example.json":"ai-event-record.schema.json","finding-ledger.example.json":"finding-ledger.schema.json","run-result.example.json":"run-result.schema.json"}
        for example_name, schema_name in examples.items():
            path = ROOT / "schemas" / "examples" / example_name
            if path.is_file() and schema_name in schema_map:
                errors.extend(f"{example_name}: {message}" for message in validate_instance(read_json(path), schema_map[schema_name], registry))
        fixture_schema = schema_map.get("fixture-contract.schema.json")
        catalog = documents.get(ROOT / "evals" / "fixture_catalog.json", {})
        if fixture_schema:
            for fixture in catalog.get("fixtures", []):
                errors.extend(f"{fixture.get('fixture_id')}: {message}" for message in validate_instance(fixture, fixture_schema, registry))
        for schema_name, template_name in [("regression-intake.schema.json","regression-intake.template.json"),("production-failure.schema.json","production-failure.template.json")]:
            schema = schema_map.get(schema_name)
            template = ROOT / "CHANGELOG_REGRESSION" / template_name
            if schema and template.is_file():
                errors.extend(f"{template_name}: {message}" for message in validate_instance(read_json(template), schema, registry))

    ruleset = documents.get(ROOT / "02_RULES" / "ruleset.json", {})
    rules = ruleset.get("rules", [])
    rule_ids = [rule.get("id") for rule in rules]
    if len(rules) != 30:
        errors.append(f"expected 30 SEI rules, found {len(rules)}")
    if len(set(rule_ids)) != len(rule_ids):
        errors.append("SEI rule IDs are not unique")
    if any(rule.get("formal_allegation_allowed") is not False for rule in rules):
        errors.append("every SEI rule must prohibit formal allegation inference")
    if ruleset.get("version") != "0.1.0":
        errors.append("ruleset version must be 0.1.0")
    hooks = documents.get(ROOT / "02_RULES" / "decision_hooks.json", {}).get("hooks", [])
    if len(hooks) != 9:
        errors.append(f"expected 9 SEI decision hooks, found {len(hooks)}")
    catalog = documents.get(ROOT / "evals" / "fixture_catalog.json", {})
    if len(catalog.get("fixtures", [])) != 42:
        errors.append(f"expected 42 SEI fixtures, found {len(catalog.get('fixtures', []))}")
    crosswalk = documents.get(ROOT / "evals" / "rule_fixture_crosswalk.json", {})
    if len(crosswalk.get("rows", [])) != len(rules):
        errors.append("SEI crosswalk row count does not equal rule count")
    result = {"pass":not errors,"package":"scholarly-editorial-integrity","specification_sha256":sha256(spec_path) if spec_path.is_file() else None,"rule_count":len(rules),"decision_hook_count":len(hooks),"fixture_count":len(catalog.get("fixtures", [])),"crosswalk_rows":len(crosswalk.get("rows", [])),"json_file_count":len(documents),"errors":errors,"warnings":warnings}
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
