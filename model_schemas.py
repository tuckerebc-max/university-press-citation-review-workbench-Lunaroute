from __future__ import annotations


def nullable_string(max_length: int = 2000) -> dict:
    return {"type": ["string", "null"], "maxLength": max_length}


def rci_schema(rule_ids: list[str]) -> dict:
    evidence = {
        "type": "object",
        "additionalProperties": False,
        "required": ["source_id", "locator", "relevance", "access_status"],
        "properties": {
            "source_id": {"type": "string", "minLength": 1, "maxLength": 160},
            "locator": {"type": "string", "minLength": 1, "maxLength": 500},
            "relevance": {"type": "string", "minLength": 1, "maxLength": 500},
            "access_status": {
                "type": "string",
                "enum": ["available", "candidate_provider_metadata", "source_unavailable", "not_checked"],
            },
        },
    }
    finding = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "skill_id", "rule_id", "severity", "status", "action", "confidence",
            "locator", "context_type", "exact_text", "reason", "evidence",
            "proposed_change", "author_query", "dependencies",
        ],
        "properties": {
            "skill_id": {"type": "string", "enum": [f"RCI-0{i}" for i in range(1, 8)]},
            "rule_id": {"type": "string", "enum": rule_ids},
            "severity": {"type": "string", "enum": ["critical", "high", "medium", "low", "informational"]},
            "status": {"type": "string", "enum": ["verified", "informational", "needs_review", "blocked", "not_applicable", "not_checked"]},
            "action": {"type": "string", "enum": ["SUGGEST", "FLAG", "ESCALATE", "BLOCK", "CLOSE"]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "locator": {"type": "string", "minLength": 1, "maxLength": 160},
            "context_type": {"type": "string", "enum": ["body", "table", "caption", "note", "appendix", "supplementary", "reference_list"]},
            "exact_text": {"type": "string", "maxLength": 1000},
            "reason": {"type": "string", "minLength": 1, "maxLength": 1200},
            "evidence": {"type": "array", "minItems": 1, "maxItems": 8, "items": evidence},
            "proposed_change": nullable_string(1200),
            "author_query": nullable_string(1200),
            "dependencies": {"type": "array", "maxItems": 12, "items": {"type": "string", "maxLength": 160}},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["review_summary", "release_status", "findings", "author_notes"],
        "properties": {
            "review_summary": {"type": "string", "minLength": 1, "maxLength": 1200},
            "release_status": {"type": "string", "enum": ["ready", "ready_with_conditions", "not_ready"]},
            "findings": {"type": "array", "maxItems": 200, "items": finding},
            "author_notes": {"type": "array", "maxItems": 40, "items": {"type": "string", "maxLength": 800}},
        },
    }


def sei_schema(rule_ids: list[str]) -> dict:
    finding = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "skill_id", "rule_id", "status", "risk_level", "exact_text", "locator",
            "context_type", "claim_or_object", "source_or_record", "source_access_status",
            "comparison_or_basis", "authority", "reason", "owner", "next_action",
            "confidence", "escalation", "closure_condition", "release_effect",
            "proposed_change", "author_query", "dependencies",
        ],
        "properties": {
            "skill_id": {"type": "string", "enum": [f"CEI-{i:02d}" for i in range(11)]},
            "rule_id": {"type": "string", "enum": rule_ids},
            "status": {"type": "string", "enum": ["verified", "supported_with_scope", "signal", "source_unavailable", "disputed", "referred", "resolved", "blocked"]},
            "risk_level": {"type": "string", "enum": ["low", "moderate", "high", "critical"]},
            "exact_text": {"type": "string", "maxLength": 1000},
            "locator": {"type": "string", "minLength": 1, "maxLength": 160},
            "context_type": {"type": "string", "enum": ["claim", "quote", "paraphrase", "source", "contributor", "disclosure", "entity", "status", "AI_event", "protected_record", "table", "figure"]},
            "claim_or_object": {"type": "string", "enum": ["claim", "quote", "paraphrase", "source", "contributor", "disclosure", "entity", "status", "AI_event"]},
            "source_or_record": {"type": "string", "minLength": 1, "maxLength": 500},
            "source_access_status": {"type": "string", "enum": ["local", "live", "web_only", "author_supplied", "inaccessible", "stale", "unknown", "not_applicable"]},
            "comparison_or_basis": {"type": "string", "minLength": 1, "maxLength": 1200},
            "authority": {"type": "string", "minLength": 1, "maxLength": 500},
            "reason": {"type": "string", "minLength": 1, "maxLength": 1200},
            "owner": {"type": "string", "minLength": 1, "maxLength": 200},
            "next_action": {"type": "string", "minLength": 1, "maxLength": 1200},
            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            "escalation": {"type": "string", "enum": ["none", "editor", "senior_editor", "author_group", "institution", "publisher", "legal_or_ethics", "security"]},
            "closure_condition": {"type": "string", "minLength": 1, "maxLength": 1200},
            "release_effect": {"type": "string", "enum": ["none", "track", "hold", "block"]},
            "proposed_change": nullable_string(1200),
            "author_query": nullable_string(1200),
            "dependencies": {"type": "array", "maxItems": 12, "items": {"type": "string", "maxLength": 160}},
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["review_summary", "release_status", "findings", "author_notes"],
        "properties": {
            "review_summary": {"type": "string", "minLength": 1, "maxLength": 1200},
            "release_status": {"type": "string", "enum": ["ready", "ready_with_conditions", "not_ready"]},
            "findings": {"type": "array", "maxItems": 200, "items": finding},
            "author_notes": {"type": "array", "maxItems": 40, "items": {"type": "string", "maxLength": 800}},
        },
    }
