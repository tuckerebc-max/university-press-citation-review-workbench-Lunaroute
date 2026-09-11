from __future__ import annotations

import hashlib
import ipaddress
import os
import re
import socket
import stat
import urllib.parse
import zipfile
from dataclasses import dataclass
from pathlib import Path

from lxml import etree

from . import config


class SafetyError(ValueError):
    pass


@dataclass(frozen=True)
class SourceFile:
    path: Path
    relative_path: str
    size: int
    sha256: str


def _is_reparse_point(path: Path) -> bool:
    info = path.lstat()
    attrs = getattr(info, "st_file_attributes", 0)
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return path.is_symlink() or bool(attrs & flag)


def sha256_file(path: Path) -> str:
    before = path.lstat()
    if _is_reparse_point(path):
        raise SafetyError(f"Symlink or reparse-point input is not allowed: {path.name}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        if (before.st_dev, before.st_ino, before.st_size) != (
            opened.st_dev,
            opened.st_ino,
            opened.st_size,
        ):
            raise SafetyError(f"Source changed while opening: {path.name}")
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.lstat()
    if (before.st_mtime_ns, before.st_size) != (after.st_mtime_ns, after.st_size):
        raise SafetyError(f"Source changed while hashing: {path.name}")
    return digest.hexdigest()


def read_approved_bytes(path: Path, expected_sha256: str) -> bytes:
    """Read one approved source snapshot without following a late path swap."""
    before = path.lstat()
    if _is_reparse_point(path):
        raise SafetyError(f"Symlink or reparse-point input is not allowed: {path.name}")
    if before.st_size > config.MAX_FILE_BYTES:
        raise SafetyError(f"{path.name} exceeds the approved file-size limit.")
    digest = hashlib.sha256()
    chunks: list[bytes] = []
    with path.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        if (before.st_dev, before.st_ino, before.st_size) != (opened.st_dev, opened.st_ino, opened.st_size):
            raise SafetyError(f"Source changed while opening: {path.name}")
        total = 0
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            total += len(chunk)
            if total > config.MAX_FILE_BYTES:
                raise SafetyError(f"{path.name} exceeded the approved file-size limit while reading.")
            digest.update(chunk)
            chunks.append(chunk)
    after = path.lstat()
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    ):
        raise SafetyError(f"Source changed while reading: {path.name}")
    if digest.hexdigest() != expected_sha256:
        raise SafetyError(f"Source no longer matches the approved manifest: {path.name}")
    return b"".join(chunks)


def validate_input_root(value: str | Path) -> Path:
    raw = Path(value).expanduser()
    if not raw.is_absolute():
        raise SafetyError("The chapter folder must be an absolute path.")
    if not raw.exists() or not raw.is_dir():
        raise SafetyError("The chapter folder does not exist or is not a directory.")
    if _is_reparse_point(raw):
        raise SafetyError("A symlinked or reparse-point chapter folder is not allowed.")
    return raw.resolve(strict=True)


def validate_output_parent(value: str | Path, input_root: Path) -> Path:
    raw = Path(value).expanduser()
    if not raw.is_absolute():
        raise SafetyError("The output folder must be an absolute path.")
    if not raw.exists() or not raw.is_dir():
        raise SafetyError("The output parent folder does not exist.")
    if _is_reparse_point(raw):
        raise SafetyError("A symlinked or reparse-point output folder is not allowed.")
    resolved = raw.resolve(strict=True)
    try:
        resolved.relative_to(input_root)
    except ValueError:
        pass
    else:
        raise SafetyError("The output folder cannot be inside the source folder.")
    return resolved


def scan_sources(root: Path) -> list[SourceFile]:
    sources: list[SourceFile] = []
    total = 0
    pending = [root]
    while pending:
        directory = pending.pop()
        if _is_reparse_point(directory):
            continue
        for entry in os.scandir(directory):
            path = Path(entry.path)
            if entry.is_symlink():
                continue
            if entry.is_dir(follow_symlinks=False):
                if not _is_reparse_point(path):
                    pending.append(path)
                continue
            if not entry.is_file(follow_symlinks=False):
                continue
            if path.name.startswith("~$") or path.suffix.lower() not in config.SUPPORTED_EXTENSIONS:
                continue
            size = entry.stat(follow_symlinks=False).st_size
            if size <= 0:
                continue
            if size > config.MAX_FILE_BYTES:
                raise SafetyError(f"{path.name} exceeds the {config.MAX_FILE_BYTES // 1024 // 1024} MB limit.")
            total += size
            if total > config.MAX_TOTAL_BYTES:
                raise SafetyError("The selected chapter set exceeds the total size limit.")
            relative = path.resolve(strict=True).relative_to(root).as_posix()
            sources.append(SourceFile(path, relative, size, sha256_file(path)))
            if len(sources) > config.MAX_CHAPTERS:
                raise SafetyError(f"A run may contain at most {config.MAX_CHAPTERS} chapters.")
    return sorted(sources, key=lambda item: item.relative_path.casefold())


def validate_docx_archive(path: Path) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            members = archive.infolist()
            if len(members) > config.MAX_DOCX_MEMBERS:
                raise SafetyError("DOCX contains too many archive members.")
            names: set[str] = set()
            actual_names: set[str] = set()
            expanded = 0
            for item in members:
                normalized = item.filename.replace("\\", "/")
                parts = [part for part in normalized.split("/") if part]
                if normalized.startswith("/") or ".." in parts:
                    raise SafetyError("DOCX contains an unsafe archive path.")
                folded = normalized.casefold()
                if folded in names:
                    raise SafetyError("DOCX contains duplicate archive member names.")
                names.add(folded)
                actual_names.add(normalized)
                if item.flag_bits & 0x1:
                    raise SafetyError("Encrypted DOCX archive members are not allowed.")
                if item.file_size > config.MAX_DOCX_MEMBER_BYTES:
                    raise SafetyError("DOCX contains an oversized archive member.")
                expanded += item.file_size
                if expanded > config.MAX_DOCX_EXPANDED_BYTES:
                    raise SafetyError("DOCX expanded size exceeds the safety limit.")
                if item.file_size and not item.compress_size:
                    raise SafetyError("DOCX contains an invalid zero-size compressed member.")
                if item.compress_size and item.file_size / item.compress_size > 250:
                    raise SafetyError("DOCX contains a suspicious compression ratio.")
                if folded.startswith(("word/embeddings/", "word/activex/", "customui/")) or folded == "word/vbaproject.bin":
                    raise SafetyError("DOCX contains active or embedded content that must be flattened before review.")
            if "[Content_Types].xml" not in actual_names or "word/document.xml" not in actual_names:
                raise SafetyError("File is not a valid Word document package.")
            for item in members:
                xml_name = item.filename.replace("\\", "/")
                if xml_name.casefold().endswith((".xml", ".rels")):
                    sample = archive.read(item)
                    upper = sample.upper()
                    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
                        raise SafetyError("DOCX contains disallowed XML declarations.")
                    if xml_name.casefold().endswith(".rels"):
                        try:
                            relationships = etree.fromstring(sample, parser=etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False, recover=False, huge_tree=False))
                        except etree.XMLSyntaxError as exc:
                            raise SafetyError("DOCX contains an invalid relationships file.") from exc
                        for relationship in relationships:
                            if relationship.attrib.get("TargetMode") != "External":
                                continue
                            relationship_type = relationship.attrib.get("Type", "")
                            target = relationship.attrib.get("Target", "")
                            parsed = urllib.parse.urlsplit(target)
                            safe_hyperlink = (
                                relationship_type.endswith("/hyperlink")
                                and parsed.scheme.casefold() in {"http", "https", "mailto"}
                                and len(target) <= 2048
                                and not parsed.username
                                and not parsed.password
                            )
                            if not safe_hyperlink:
                                raise SafetyError("DOCX contains a disallowed external relationship.")
    except zipfile.BadZipFile as exc:
        raise SafetyError("File is not a readable DOCX package.") from exc


def assert_public_dns(host: str) -> None:
    if host not in config.ALLOWED_EGRESS_HOSTS:
        raise SafetyError("Network host is not allowlisted.")
    addresses = {item[4][0] for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)}
    if not addresses:
        raise SafetyError("Network host did not resolve.")
    for value in addresses:
        address = ipaddress.ip_address(value)
        if not address.is_global:
            raise SafetyError("Network host resolved to a non-public address.")


def safe_slug(value: str, fallback: str = "chapter") -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    return (value[:80] or fallback).lower()


def scrub_message(message: object, secret: str | None = None) -> str:
    text = str(message)
    if secret:
        text = text.replace(secret, "[REDACTED]")
    text = re.sub(r"(?i)(authorization\s*:\s*bearer\s+)[^\s]+", r"\1[REDACTED]", text)
    text = re.sub(r"\blr_[A-Za-z0-9_-]{20,}\b", "[REDACTED]", text)
    return text[:800]
