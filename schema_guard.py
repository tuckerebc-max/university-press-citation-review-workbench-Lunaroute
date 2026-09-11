from __future__ import annotations

from typing import Any


class SchemaViolation(ValueError):
    pass


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    """Validate the JSON-schema subset used by this workbench without coercion."""
    if "const" in schema and instance != schema["const"]:
        raise SchemaViolation(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaViolation(f"{path}: value is outside the allowed vocabulary")

    expected = schema.get("type")
    if isinstance(expected, list):
        errors = []
        for candidate in expected:
            try:
                validate(instance, {**schema, "type": candidate}, path)
                return
            except SchemaViolation as exc:
                errors.append(str(exc))
        raise SchemaViolation(f"{path}: value does not match any allowed type")

    if expected == "object":
        if not isinstance(instance, dict):
            raise SchemaViolation(f"{path}: expected object")
        required = set(schema.get("required", []))
        missing = sorted(required - instance.keys())
        if missing:
            raise SchemaViolation(f"{path}: missing required fields {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise SchemaViolation(f"{path}: unexpected fields {extras}")
        for key, value in instance.items():
            if key in properties:
                validate(value, properties[key], f"{path}.{key}")
        return

    if expected == "array":
        if not isinstance(instance, list):
            raise SchemaViolation(f"{path}: expected array")
        if len(instance) < schema.get("minItems", 0):
            raise SchemaViolation(f"{path}: too few items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise SchemaViolation(f"{path}: too many items")
        item_schema = schema.get("items")
        if item_schema:
            for index, value in enumerate(instance):
                validate(value, item_schema, f"{path}[{index}]")
        return

    if expected == "string":
        if not isinstance(instance, str):
            raise SchemaViolation(f"{path}: expected string")
        if len(instance) < schema.get("minLength", 0):
            raise SchemaViolation(f"{path}: string is too short")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            raise SchemaViolation(f"{path}: string is too long")
        return
    if expected == "integer":
        if isinstance(instance, bool) or not isinstance(instance, int):
            raise SchemaViolation(f"{path}: expected integer")
    elif expected == "number":
        if isinstance(instance, bool) or not isinstance(instance, (int, float)):
            raise SchemaViolation(f"{path}: expected number")
    elif expected == "boolean":
        if not isinstance(instance, bool):
            raise SchemaViolation(f"{path}: expected boolean")
        return
    elif expected == "null":
        if instance is not None:
            raise SchemaViolation(f"{path}: expected null")
        return
    elif expected is None:
        return

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise SchemaViolation(f"{path}: below minimum")
        if "maximum" in schema and instance > schema["maximum"]:
            raise SchemaViolation(f"{path}: above maximum")
