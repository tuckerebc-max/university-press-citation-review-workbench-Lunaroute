#!/usr/bin/env python3
"""Deterministic validation and scoring for the MWM RCI synthetic gold suite.

The scorer intentionally does not judge prose similarity. It compares a candidate
run's structured rule IDs, actions, statuses, release status, hooks, and routes to
the gold contract. Use --validate-suite before scoring any candidate output.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
RULES = ROOT / "02_RULES"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_suite() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], set[str]]:
    catalog = load_json(EVALS / "fixture_catalog.json")
    crosswalk = load_json(EVALS / "rule_fixture_crosswalk.json")
    main_rules = load_json(RULES / "ruleset.json")
    addenda = load_json(RULES / "ruleset_addenda.json")
    rule_ids = {rule["id"] for rule in main_rules["rules"]}
    rule_ids.update(rule["id"] for rule in addenda["rules"])
    return catalog, crosswalk, main_rules, rule_ids


def fixture_map(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {fixture["fixture_id"]: fixture for fixture in catalog["fixtures"]}


def validate_suite() -> list[str]:
    errors: list[str] = []
    catalog, crosswalk, _, rule_ids = load_suite()
    fixtures = fixture_map(catalog)

    if catalog.get("evaluation_set_id") != crosswalk.get("evaluation_set_id"):
        errors.append("catalog and crosswalk evaluation_set_id values differ")
    if len(fixtures) != len(catalog.get("fixtures", [])):
        errors.append("fixture IDs are not unique")

    counts = Counter(fixture.get("kind") for fixture in catalog.get("fixtures", []))
    for kind, expected in catalog.get("fixture_counts", {}).items():
        if counts[kind] != expected:
            errors.append(f"fixture count for {kind!r}: expected {expected}, found {counts[kind]}")

    for fixture_id, fixture in fixtures.items():
        required = {"fixture_id", "kind", "title", "synthetic", "input", "gold"}
        missing = required - fixture.keys()
        if missing:
            errors.append(f"{fixture_id}: missing fields {sorted(missing)}")
        if fixture.get("synthetic") is not True:
            errors.append(f"{fixture_id}: fixture is not marked synthetic=true")
        gold = fixture.get("gold", {})
        for field in ("expected_release_status", "expected_rule_ids", "expected_actions", "must_not_emit_rule_ids"):
            if field not in gold:
                errors.append(f"{fixture_id}: gold.{field} is required")
        for rule_id in gold.get("expected_rule_ids", []) + gold.get("must_not_emit_rule_ids", []):
            if rule_id not in rule_ids:
                errors.append(f"{fixture_id}: references unknown rule {rule_id}")

    crosswalk_rows = crosswalk.get("rows", [])
    crosswalk_rule_ids = set()
    for row in crosswalk_rows:
        rule_id = row.get("rule_id")
        crosswalk_rule_ids.add(rule_id)
        if rule_id not in rule_ids:
            errors.append(f"crosswalk references unknown rule {rule_id}")
        for category in crosswalk.get("coverage_policy", {}).get("required_fixture_classes", []):
            if not row.get(category):
                errors.append(f"{rule_id}: missing required crosswalk category {category}")
        seen_in_row: set[str] = set()
        for category, ids in row.items():
            if category == "rule_id":
                continue
            if not isinstance(ids, list):
                errors.append(f"{rule_id}.{category}: expected a list")
                continue
            for fixture_id in ids:
                if fixture_id not in fixtures:
                    errors.append(f"{rule_id}.{category}: unknown fixture {fixture_id}")
                if fixture_id in seen_in_row:
                    errors.append(f"{rule_id}: fixture {fixture_id} is repeated across crosswalk categories")
                seen_in_row.add(fixture_id)

    missing_crosswalk = rule_ids - crosswalk_rule_ids
    if missing_crosswalk:
        errors.append(f"rules missing from crosswalk: {sorted(missing_crosswalk)}")

    integration_ids = {fixture["fixture_id"] for fixture in catalog["fixtures"] if fixture["kind"] == "integration"}
    integration_cases = load_json(EVALS / "integration_cases.json")
    listed_integration = {case["fixture_id"] for case in integration_cases.get("cases", [])}
    if integration_ids != listed_integration:
        errors.append("integration_cases.json does not list exactly the catalog integration fixtures")

    controls = load_json(EVALS / "adversarial_negative_controls.json")
    if set(controls.get("adversarial_fixture_ids", [])) != {fixture["fixture_id"] for fixture in catalog["fixtures"] if fixture["kind"] == "adversarial"}:
        errors.append("adversarial control list does not match catalog")
    if set(controls.get("negative_control_fixture_ids", [])) != {fixture["fixture_id"] for fixture in catalog["fixtures"] if fixture["kind"] == "negative_control"}:
        errors.append("negative control list does not match catalog")

    return errors


def score_candidate(candidate_path: Path) -> dict[str, Any]:
    catalog, _, _, _ = load_suite()
    fixtures = fixture_map(catalog)
    candidate = load_json(candidate_path)
    results = {result["fixture_id"]: result for result in candidate.get("results", [])}
    rows: list[dict[str, Any]] = []
    passed = 0

    for fixture_id, fixture in fixtures.items():
        gold = fixture["gold"]
        result = results.get(fixture_id)
        problems: list[str] = []
        if result is None:
            problems.append("missing candidate result")
            result = {}
        detected = set(result.get("detected_rule_ids", []))
        expected = set(gold.get("expected_rule_ids", []))
        forbidden = set(gold.get("must_not_emit_rule_ids", []))
        missing = sorted(expected - detected)
        unexpected = sorted(detected - expected - set(gold.get("allowed_extra_rule_ids", [])))
        forbidden_hits = sorted(detected & forbidden)
        if missing:
            problems.append(f"missing expected rules: {missing}")
        if unexpected:
            problems.append(f"unexpected rules: {unexpected}")
        if forbidden_hits:
            problems.append(f"forbidden rules: {forbidden_hits}")
        if result.get("release_status") != gold.get("expected_release_status"):
            problems.append(f"release status {result.get('release_status')!r} != {gold.get('expected_release_status')!r}")
        for action in gold.get("expected_actions", []):
            if action not in set(result.get("actions", [])):
                problems.append(f"missing expected action: {action}")
        for status in gold.get("expected_statuses", []):
            if status not in set(result.get("statuses", [])):
                problems.append(f"missing expected status: {status}")
        for hook in gold.get("required_decision_hooks", []):
            if hook not in set(result.get("decision_hooks", [])):
                problems.append(f"missing required decision hook: {hook}")
        for route in gold.get("expected_routes", []):
            if route not in set(result.get("routes", [])):
                problems.append(f"missing expected route: {route}")
        row = {"fixture_id": fixture_id, "passed": not problems, "problems": problems}
        rows.append(row)
        if not problems:
            passed += 1

    unknown_results = sorted(set(results) - set(fixtures))
    if unknown_results:
        rows.append({"fixture_id": "<candidate-extra>", "passed": False, "problems": [f"unknown fixture IDs: {unknown_results}"]})

    rule_hits = Counter(rule_id for result in results.values() for rule_id in result.get("detected_rule_ids", []))
    zero_tolerance = [fixture_id for fixture_id, fixture in fixtures.items() if fixture["gold"].get("zero_tolerance")]
    zero_tolerance_passed = sum(1 for row in rows if row["fixture_id"] in zero_tolerance and row["passed"])
    total = len(fixtures)
    return {
        "evaluation_set_id": catalog["evaluation_set_id"],
        "candidate": str(candidate_path),
        "fixtures_total": total,
        "fixtures_passed": passed,
        "fixture_accuracy": round(passed / total, 4) if total else 0.0,
        "zero_tolerance_total": len(zero_tolerance),
        "zero_tolerance_passed": zero_tolerance_passed,
        "rule_hits": dict(sorted(rule_hits.items())),
        "unknown_candidate_fixtures": unknown_results,
        "rows": rows,
        "pass": passed == total and not unknown_results and zero_tolerance_passed == len(zero_tolerance)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--validate-suite", action="store_true")
    group.add_argument("--score", type=Path, metavar="CANDIDATE_JSON")
    args = parser.parse_args()

    try:
        errors = validate_suite()
        if errors:
            print(json.dumps({"pass": False, "errors": errors}, indent=2))
            return 1
        if args.validate_suite:
            catalog, crosswalk, _, rule_ids = load_suite()
            print(json.dumps({"pass": True, "evaluation_set_id": catalog["evaluation_set_id"], "fixture_count": len(catalog["fixtures"]), "rule_count": len(rule_ids), "crosswalk_rows": len(crosswalk["rows"])}, indent=2))
            return 0
        result = score_candidate(args.score)
        print(json.dumps(result, indent=2))
        return 0 if result["pass"] else 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(json.dumps({"pass": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
