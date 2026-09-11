from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "data"}
PATTERNS = {
    "LunaRoute-like token": re.compile(rb"\blr_[A-Za-z0-9_-]{20,}\b"),
    "OpenAI-like token": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "Google API key": re.compile(rb"\bAIza[0-9A-Za-z_-]{20,}\b"),
    "private key": re.compile(rb"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}


def main() -> int:
    findings: list[tuple[str, str]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or EXCLUDED_PARTS.intersection(path.parts) or path.suffix in {".pyc", ".pyo"}:
            continue
        try:
            payload = path.read_bytes()
        except OSError:
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(payload):
                findings.append((path.relative_to(ROOT).as_posix(), label))
    if findings:
        for path, label in findings:
            print(f"{path}: potential {label}")
        return 1
    print("No token or private-key patterns detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
