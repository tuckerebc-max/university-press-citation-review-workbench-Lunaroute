from __future__ import annotations

import re
import unicodedata
from typing import Any

from .ingest import Chapter

YEAR_RE = re.compile(r"\b((?:19|20)\d{2}[a-z]?)\b", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
PAREN_RE = re.compile(r"\(([^()]{0,300}?\b(?:19|20)\d{2}[a-z]?\b[^()]{0,180})\)")
NARRATIVE_RE = re.compile(r"\b([A-Z][A-Za-zÀ-ÖØ-öø-ÿ\u2019'\-]+(?:\s+et\s+al\.)?)\s*\(((?:19|20)\d{2}[a-z]?)\)")


def _normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _first_author(value: str) -> str:
    value = re.sub(r"\bet\s+al\.?", "", value, flags=re.IGNORECASE).strip()
    value = re.split(r"[,&;]", value, maxsplit=1)[0]
    tokens = _normalized(value).split()
    return tokens[-1] if tokens else ""


def _reference_record(text: str, locator: str, number: int) -> dict[str, Any]:
    year_match = YEAR_RE.search(text)
    year = year_match.group(1) if year_match else None
    author_text = text[: year_match.start()] if year_match else text.split(".", 1)[0]
    author = _first_author(author_text)
    remainder = text[year_match.end() :] if year_match else text
    title_bits = [part.strip(" .()") for part in remainder.split(".") if part.strip(" .()")]
    title = title_bits[0] if title_bits else None
    identifiers = []
    for doi in sorted({match.group(0).rstrip(".,;)") for match in DOI_RE.finditer(text)}, key=str.casefold):
        identifiers.append({"scheme": "doi", "raw": doi, "normalized": doi.lower(), "status": "syntax_only"})
    return {
        "reference_id": f"R{number:03d}",
        "raw_text": text,
        "location": locator,
        "source_type": "unknown_or_ambiguous",
        "authors_or_group": [author] if author else [],
        "date": year,
        "title": title,
        "container_title": None,
        "version": None,
        "edition": None,
        "identifiers": identifiers,
        "metadata_provenance": [],
        "parse_confidence": 0.75 if author and year else 0.45,
    }


def _citation_record(raw: str, locator: str, number: int, form: str) -> dict[str, Any]:
    year = YEAR_RE.search(raw)
    before = raw[: year.start()] if year else raw
    author = _first_author(before)
    locator_match = re.search(r"\b(?:p{1,2}\.|para\.|chapter|table|figure)\s*\d+[A-Za-z-]*", raw, re.IGNORECASE)
    return {
        "citation_id": f"C{number:03d}",
        "raw_text": raw,
        "location": locator,
        "context_type": "body",
        "citation_form": form,
        "authors_or_group": [author] if author else [],
        "year": year.group(1) if year else None,
        "locator": locator_match.group(0) if locator_match else None,
        "quotation_detected": False,
        "candidate_reference_ids": [],
        "parse_confidence": 0.8 if author and year else 0.5,
    }


def build_inventory(chapter: Chapter) -> dict[str, Any]:
    references = []
    for block in chapter.blocks:
        heading_candidate = block.text.casefold().strip().lstrip("#").strip().rstrip(":").strip()
        if block.in_references and heading_candidate not in {"references", "bibliography", "works cited", "reference list", "literature cited"}:
            references.append(_reference_record(block.text, block.locator, len(references) + 1))

    citations = []
    seen_spans: set[tuple[str, int, int]] = set()
    for block in chapter.blocks:
        if block.in_references:
            continue
        for match in PAREN_RE.finditer(block.text):
            pieces = [piece.strip() for piece in match.group(1).split(";") if YEAR_RE.search(piece)]
            for piece in pieces:
                citations.append(_citation_record(f"({piece})", block.locator, len(citations) + 1, "parenthetical"))
            seen_spans.add((block.locator, match.start(), match.end()))
        for match in NARRATIVE_RE.finditer(block.text):
            if any(loc == block.locator and start <= match.start() < end for loc, start, end in seen_spans):
                continue
            citations.append(_citation_record(match.group(0), block.locator, len(citations) + 1, "narrative"))

    ref_by_key: dict[tuple[str, str], list[str]] = {}
    for ref in references:
        key = ((ref["authors_or_group"] or [""])[0], ref["date"] or "")
        ref_by_key.setdefault(key, []).append(ref["reference_id"])

    unmatched = []
    for citation in citations:
        key = ((citation["authors_or_group"] or [""])[0], citation["year"] or "")
        candidates = ref_by_key.get(key, [])
        citation["candidate_reference_ids"] = candidates
        if not candidates:
            unmatched.append(citation["citation_id"])

    ledgers = []
    cited_reference_ids = {rid for citation in citations for rid in citation["candidate_reference_ids"]}
    for index, ref in enumerate(references, 1):
        citation_ids = [c["citation_id"] for c in citations if ref["reference_id"] in c["candidate_reference_ids"]]
        status = "orphan_reference" if not citation_ids else "matched"
        if any(len(c["candidate_reference_ids"]) > 1 for c in citations if c["citation_id"] in citation_ids):
            status = "ambiguous_match"
        ledgers.append({
            "ledger_entry_id": f"L{index:03d}",
            "source_record_id": ref["reference_id"],
            "citation_ids": citation_ids,
            "reference_ids": [ref["reference_id"]],
            "relationship_status": status,
            "match_method": "exact_author_year" if status == "matched" else "none",
            "candidate_source_record_ids": [],
            "confidence": 0.85 if status == "matched" else 0.45,
            "evidence_ids": [f"MANUSCRIPT-{chapter.chapter_id}"],
            "exception_id": None,
            "decision_log_id": None,
        })

    dois = sorted({identifier["normalized"] for ref in references for identifier in ref["identifiers"]})
    return {
        "schema_version": 1,
        "chapter_id": chapter.chapter_id,
        "citations": citations,
        "references": references,
        "ledger_entries": ledgers,
        "unmatched_citation_ids": unmatched,
        "orphan_reference_ids": sorted(ref["reference_id"] for ref in references if ref["reference_id"] not in cited_reference_ids),
        "dois": dois,
        "parser_coverage": chapter.parser_coverage,
        "coverage_notes": chapter.coverage_notes,
    }
