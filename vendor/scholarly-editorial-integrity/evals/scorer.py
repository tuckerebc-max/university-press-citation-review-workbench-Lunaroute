#!/usr/bin/env python3
"""Validate and score the synthetic Scholarly/Editorial Integrity suite."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def suite_objects() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        load_json(EVALS / "fixture_catalog.json"),
        load_json(EVALS / "rule_fixture_crosswalk.json"),
        load_json(EVALS / "adversarial_negative_controls.json"),
        load_json(EVALS / "integration_cases.json"),
        load_json(ROOT / "02_RULES" / "ruleset.json"),
    )


def validate_suite() -> dict[str, Any]:
    catalog, crosswalk, controls, integrations, ruleset = suite_objects()
    fixtures = catalog.get("fixtures", [])
    fixture_map = {item.get("fixture_id"): item for item in fixtures}
    rule_ids = [rule.get("id") for rule in ruleset.get("rules", [])]
    errors: list[str] = []
    if len(fixture_map) != len(fixtures):
        errors.append("fixture IDs are not unique")
    if not all(item.get("synthetic") is True for item in fixtures):
        errors.append("every fixture must be synthetic=true")
    actual_counts = Counter(item.get("kind") for item in fixtures)
    for kind, expected in catalog.get("fixture_counts", {}).items():
        if actual_counts.get(kind, 0) != expected:
            errors.append(f"fixture count for {kind}: expected {expected}, got {actual_counts.get(kind, 0)}")
    for fixture in fixtures:
        gold = fixture.get("gold", {})
        unknown = (set(gold.get("expected_rule_ids", [])) | set(gold.get("must_not_emit_rule_ids", []))) - set(rule_ids)
        if unknown:
            errors.append(f"{fixture.get('fixture_id')}: unknown rule IDs {sorted(unknown)}")
        if not gold.get("expected_release_status"):
            errors.append(f"{fixture.get('fixture_id')}: missing expected release status")
    rows = crosswalk.get("rows", [])
    row_ids = [row.get("rule_id") for row in rows]
    if len(set(row_ids)) != len(row_ids):
        errors.append("crosswalk rule IDs are not unique")
    if set(row_ids) != set(rule_ids):
        errors.append("crosswalk does not cover exactly the ruleset")
    for row in rows:
        for column in ("positive", "negative", "adversarial"):
            values = row.get(column, [])
            if not values:
                errors.append(f"{row.get('rule_id')}: missing {column} fixture")
            for fixture_id in values:
                if fixture_id not in fixture_map:
                    errors.append(f"{row.get('rule_id')}: unknown fixture {fixture_id}")
        for fixture_id in row.get("integration", []):
            if fixture_id not in fixture_map or fixture_map[fixture_id].get("kind") != "integration":
                errors.append(f"{row.get('rule_id')}: invalid integration fixture {fixture_id}")
    if set(controls.get("adversarial_fixture_ids", [])) != {item["fixture_id"] for item in fixtures if item.get("kind") == "adversarial"}:
        errors.append("adversarial controls do not match catalog")
    if set(controls.get("negative_control_fixture_ids", [])) != {item["fixture_id"] for item in fixtures if item.get("kind") == "negative_control"}:
        errors.append("negative controls do not match catalog")
    if {case.get("fixture_id") for case in integrations.get("cases", [])} != {item["fixture_id"] for item in fixtures if item.get("kind") == "integration"}:
        errors.append("integration cases do not match catalog")
    return {"pass":not errors,"evaluation_set_id":catalog.get("evaluation_set_id"),"fixture_count":len(fixtures),"fixture_counts":dict(actual_counts),"rule_count":len(rule_ids),"crosswalk_rows":len(rows),"errors":errors}


def as_set(value: Any) -> set[str]:
    return {str(item) for item in (value or [])}


def score_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    catalog, _, _, _, _ = suite_objects()
    fixtures = {item["fixture_id"]: item for item in catalog.get("fixtures", [])}
    results = {item.get("fixture_id"): item for item in candidate.get("results", [])}
    details: list[dict[str, Any]] = []
    zero_total = 0
    zero_passed = 0
    for fixture_id, fixture in fixtures.items():
        gold = fixture["gold"]
        result = results.get(fixture_id, {})
        expected_rules = as_set(gold.get("expected_rule_ids"))
        emitted_rules = as_set(result.get("detected_rule_ids"))
        forbidden_rules = as_set(gold.get("must_not_emit_rule_ids"))
        expected_interventions = as_set(gold.get("expected_interventions"))
        actual_interventions = as_set(result.get("interventions"))
        expected_statuses = as_set(gold.get("expected_statuses"))
        actual_statuses = as_set(result.get("statuses"))
        expected_hooks = as_set(gold.get("required_decision_hooks"))
        actual_hooks = as_set(result.get("decision_hooks"))
        expected_routes = as_set(gold.get("expected_routes"))
        actual_routes = as_set(result.get("routes"))
        mismatches: list[str] = []
        if result.get("release_status") != gold.get("expected_release_status"):
            mismatches.append("release_status")
        if not expected_rules.issubset(emitted_rules):
            mismatches.append("missing_expected_rule_ids")
        if forbidden_rules & emitted_rules:
            mismatches.append("forbidden_rule_ids_emitted")
        if not expected_interventions.issubset(actual_interventions):
            mismatches.append("missing_expected_interventions")
        if expected_statuses and not expected_statuses.issubset(actual_statuses):
            mismatches.append("missing_expected_statuses")
        if expected_hooks and not expected_hooks.issubset(actual_hooks):
            mismatches.append("missing_required_decision_hooks")
        if expected_routes and not expected_routes.issubset(actual_routes):
            mismatches.append("missing_expected_routes")
        passed = not mismatches
        if gold.get("zero_tolerance"):
            zero_total += 1
            if passed:
                zero_passed += 1
        details.append({"fixture_id":fixture_id,"pass":passed,"mismatches":mismatches})
    unknown_ids = sorted(set(results) - set(fixtures))
    if unknown_ids:
        details.append({"fixture_id":"<candidate>","pass":False,"mismatches":[f"unknown_fixture_ids:{','.join(unknown_ids)}"]})
    passed_count = sum(1 for item in details if item["pass"])
    return {"pass":passed_count == len(fixtures) and not unknown_ids,"fixture_count":len(fixtures),"scored_count":len(results),"passed_count":passed_count,"accuracy":round(passed_count / len(fixtures),6) if fixtures else 0.0,"zero_tolerance":{"passed":zero_passed,"total":zero_total},"details":details}


def synthetic_gold_candidate() -> dict[str, Any]:
    catalog, _, _, _, _ = suite_objects()
    return {"candidate_id":"synthetic-gold-self-test","results":[
        {"fixture_id":fixture["fixture_id"],"detected_rule_ids":fixture["gold"].get("expected_rule_ids",[]),"release_status":fixture["gold"]["expected_release_status"],"interventions":fixture["gold"].get("expected_interventions",[]),"statuses":fixture["gold"].get("expected_statuses",[]),"decision_hooks":fixture["gold"].get("required_decision_hooks",[]),"routes":fixture["gold"].get("expected_routes",[])}
        for fixture in catalog.get("fixtures", [])
    ]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate-suite",action="store_true",help="validate fixture, crosswalk, and control coverage")
    parser.add_argument("--self-test",action="store_true",help="score the catalog's in-memory gold expectations")
    parser.add_argument("--score",type=Path,help="score a candidate JSON file")
    args = parser.parse_args()
    if not args.validate_suite and not args.self_test and not args.score:
        parser.error("choose --validate-suite, --self-test, or --score")
    output: dict[str, Any] = {}
    if args.validate_suite:
        output["suite_validation"] = validate_suite()
    if args.self_test:
        output["self_test"] = score_candidate(synthetic_gold_candidate())
    if args.score:
        output["candidate_score"] = score_candidate(load_json(args.score))
    print(json.dumps(output,indent=2,sort_keys=True))
    return 0 if all(section.get("pass") for section in output.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
