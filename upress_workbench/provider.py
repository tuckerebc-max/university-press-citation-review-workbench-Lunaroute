from __future__ import annotations

import json
import os
import secrets
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from . import config
from .schema_guard import SchemaViolation, validate
from .security import SafetyError, assert_public_dns, scrub_message


class ProviderError(RuntimeError):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class CallBudget:
    max_calls: int
    max_input_chars: int

    def __post_init__(self) -> None:
        self.calls = 0
        self.input_chars = 0
        self._lock = threading.Lock()

    def reserve(self, input_chars: int) -> None:
        with self._lock:
            if self.calls + 1 > self.max_calls:
                raise ProviderError("The run model-call budget has been exhausted.")
            if self.input_chars + input_chars > self.max_input_chars:
                raise ProviderError("The run model-input budget has been exhausted.")
            self.calls += 1
            self.input_chars += input_chars

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return {"calls": self.calls, "input_chars": self.input_chars, "max_calls": self.max_calls, "max_input_chars": self.max_input_chars}


class LunaRouteClient:
    def __init__(self, model: str, budget: CallBudget, timeout: int = 300) -> None:
        if model not in config.ALLOWED_MODELS:
            raise SafetyError("Requested model is not allowlisted.")
        self.model = model
        self.budget = budget
        self.timeout = timeout
        self._opener = urllib.request.build_opener(_NoRedirect(), urllib.request.HTTPSHandler())

    def complete_json(self, system_prompt: str, user_prompt: str, schema_name: str, schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        key = os.environ.get("LUNAROUTE_API_KEY", "").strip()
        if not key:
            raise ProviderError("LUNAROUTE_API_KEY is not available in the process environment.")
        self.budget.reserve(len(system_prompt) + len(user_prompt))
        assert_public_dns(urlparse(config.LUNAROUTE_ENDPOINT).hostname or "")
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "reasoning_effort": "low",
            "max_completion_tokens": 16000,
            "temperature": 0,
            "response_format": {"type": "json_schema", "json_schema": {"name": schema_name, "strict": True, "schema": schema}},
        }
        request_bytes = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        request = urllib.request.Request(
            config.LUNAROUTE_ENDPOINT,
            data=request_bytes,
            method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": f"UniversityPressWorkbench/{config.APP_VERSION}"},
        )
        last_error = "unknown provider failure"
        for attempt in range(1, 4):
            try:
                with self._opener.open(request, timeout=self.timeout) as response:
                    raw = response.read(8 * 1024 * 1024 + 1)
                    if len(raw) > 8 * 1024 * 1024:
                        raise ProviderError("LunaRoute response exceeded the safety limit.")
                payload = json.loads(raw.decode("utf-8"))
                content = payload["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                validate(parsed, schema)
                usage = payload.get("usage") or {}
                return parsed, {"model": self.model, "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"), "total_tokens": usage.get("total_tokens")}
            except SchemaViolation:
                raise
            except urllib.error.HTTPError as exc:
                last_error = f"LunaRoute returned HTTP {exc.code}."
                if exc.code not in {429, 500, 502, 503, 504} or attempt == 3:
                    break
                retry_after = exc.headers.get("Retry-After")
                delay = min(10.0, float(retry_after)) if retry_after and retry_after.replace(".", "", 1).isdigit() else min(8.0, 2 ** (attempt - 1) + secrets.randbelow(1000) / 1000)
                time.sleep(delay)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
                last_error = scrub_message(exc, key)
                if attempt == 3:
                    break
                time.sleep(min(8.0, 2 ** (attempt - 1) + secrets.randbelow(1000) / 1000))
        raise ProviderError(scrub_message(last_error, key))
