from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
ORIGIN_DIR = ROOT_DIR / "origin"
CHAT_UPLOADS_DIR = ORIGIN_DIR / "chat-uploads"
SUPPORTED_MANAGED_SOURCE_SUFFIXES = {".txt", ".docx"}


def ensure_managed_source_dirs() -> None:
    ORIGIN_DIR.mkdir(parents=True, exist_ok=True)
    CHAT_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    candidate = Path(filename).name.strip()
    if not candidate:
        raise ValueError("Filename is required.")
    return candidate


def validate_managed_source_suffix(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_MANAGED_SOURCE_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_MANAGED_SOURCE_SUFFIXES))
        raise ValueError(f"Unsupported file type: {suffix or '(none)'}. Supported types: {supported}.")
    return suffix


def build_chat_upload_path(filename: str, *, now: datetime | None = None) -> Path:
    ensure_managed_source_dirs()
    safe_name = sanitize_filename(filename)
    suffix = validate_managed_source_suffix(safe_name)
    stamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    stem = Path(safe_name).stem
    candidate = CHAT_UPLOADS_DIR / f"{stem}_{stamp}{suffix}"

    counter = 2
    while candidate.exists():
        candidate = CHAT_UPLOADS_DIR / f"{stem}_{stamp}_{counter}{suffix}"
        counter += 1
    return candidate


def import_chat_text_attachment(filename: str, content: str) -> Path:
    if not str(content).strip():
        raise ValueError("Uploaded text content is empty. Please re-upload the file.")

    target_path = build_chat_upload_path(filename)
    target_path.write_text(content, encoding="utf-8")
    return target_path


def import_chat_binary_attachment(filename: str, content: bytes) -> Path:
    if not content:
        raise ValueError("Uploaded file content is empty. Please re-upload the file.")

    target_path = build_chat_upload_path(filename)
    target_path.write_bytes(content)
    return target_path


def import_chat_base64_attachment(filename: str, content_base64: str) -> Path:
    if not str(content_base64).strip():
        raise ValueError("Uploaded file content is empty. Please re-upload the file.")

    try:
        payload = base64.b64decode(content_base64, validate=True)
    except Exception as exc:  # pragma: no cover - exact exception type depends on decoder
        raise ValueError("Uploaded file content is invalid base64.") from exc
    return import_chat_binary_attachment(filename, payload)
