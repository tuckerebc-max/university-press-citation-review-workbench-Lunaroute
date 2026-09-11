from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from . import config
from .security import assert_public_dns, scrub_message


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _people(value: Any) -> list[str]:
    people = []
    for item in value or []:
        if not isinstance(item, dict):
            continue
        name = " ".join(part for part in [str(item.get("given") or "").strip(), str(item.get("family") or "").strip()] if part)
        if name:
            people.append(name)
    return people


def lookup_doi(doi: str, timeout: int = 20) -> dict[str, Any]:
    assert_public_dns("api.crossref.org")
    encoded = urllib.parse.quote(doi, safe="")
    url = config.CROSSREF_ENDPOINT + encoded
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": f"UniversityPressWorkbench/{config.APP_VERSION} (metadata candidate review)"})
    opener = urllib.request.build_opener(_NoRedirect(), urllib.request.HTTPSHandler())
    queried_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(2 * 1024 * 1024 + 1)
            if len(raw) > 2 * 1024 * 1024:
                raise ValueError("Crossref response exceeded the safety limit")
        message = json.loads(raw.decode("utf-8")).get("message") or {}
        observed_doi = str(message.get("DOI") or "").lower()
        return {
            "doi": doi.lower(),
            "status": "candidate_available" if observed_doi == doi.lower() else "candidate_mismatch",
            "queried_at": queried_at,
            "provider": "Crossref",
            "provider_locator": url,
            "observed": {
                "doi": observed_doi or None,
                "title": (message.get("title") or [None])[0],
                "authors": _people(message.get("author")),
                "publisher": message.get("publisher"),
                "type": message.get("type"),
                "published": message.get("published") or message.get("published-print") or message.get("published-online"),
            },
            "boundary": "Candidate provider metadata only; not a source-identity verdict.",
        }
    except urllib.error.HTTPError as exc:
        return {"doi": doi.lower(), "status": "not_found" if exc.code == 404 else "lookup_failed", "queried_at": queried_at, "provider": "Crossref", "error": f"HTTP {exc.code}"}
    except Exception as exc:  # network and decode failures become visible evidence gaps
        return {"doi": doi.lower(), "status": "lookup_failed", "queried_at": queried_at, "provider": "Crossref", "error": scrub_message(exc)}


def lookup_many(dois: list[str], limit: int = 50) -> list[dict[str, Any]]:
    return [lookup_doi(doi) for doi in dois[:limit]]
