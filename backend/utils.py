"""
utils.py
Forensic-style evidence helpers: hashing, metadata extraction, case IDs.
"""

import hashlib
import io
import uuid
from datetime import datetime, timezone

from PIL import Image, ExifTags


def generate_hash(data: bytes) -> str:
    """Return SHA-256 hex digest of raw file bytes (chain-of-custody fingerprint)."""
    return hashlib.sha256(data).hexdigest()


def generate_case_id() -> str:
    """Human-readable, unique case identifier, e.g. CASE-2026-7F3A1C."""
    return f"CASE-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"


def extract_metadata(data: bytes, filename: str) -> dict:
    """Pull basic image metadata + any available EXIF fields."""
    img = Image.open(io.BytesIO(data))

    exif_data = {}
    try:
        raw_exif = img.getexif()
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                # Keep it JSON-serializable
                exif_data[str(tag)] = str(value)
    except Exception:
        pass

    return {
        "filename": filename,
        "width": img.width,
        "height": img.height,
        "format": img.format,
        "mode": img.mode,
        "size_bytes": len(data),
        "analyzed_at_utc": datetime.now(timezone.utc).isoformat(),
        "exif": exif_data,
    }
