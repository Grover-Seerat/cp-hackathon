# """
# utils.py
# Forensic-style evidence helpers: hashing, metadata extraction, case IDs.
# """

# import hashlib
# import io
# import uuid
# from datetime import datetime, timezone

# from PIL import Image, ExifTags


# def generate_hash(data: bytes) -> str:
#     """Return SHA-256 hex digest of raw file bytes (chain-of-custody fingerprint)."""
#     return hashlib.sha256(data).hexdigest()


# def generate_case_id() -> str:
#     """Human-readable, unique case identifier, e.g. CASE-2026-7F3A1C."""
#     return f"CASE-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"


# def extract_metadata(data: bytes, filename: str) -> dict:
#     """Pull basic image metadata + any available EXIF fields."""
#     img = Image.open(io.BytesIO(data))

#     exif_data = {}
#     try:
#         raw_exif = img.getexif()
#         if raw_exif:
#             for tag_id, value in raw_exif.items():
#                 tag = ExifTags.TAGS.get(tag_id, tag_id)
#                 # Keep it JSON-serializable
#                 exif_data[str(tag)] = str(value)
#     except Exception:
#         pass

#     return {
#         "filename": filename,
#         "width": img.width,
#         "height": img.height,
#         "format": img.format,
#         "mode": img.mode,
#         "size_bytes": len(data),
#         "analyzed_at_utc": datetime.now(timezone.utc).isoformat(),
#         "exif": exif_data,
#     }
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


# Shown ONLY when the uploaded file has no real EXIF data (very common —
# WhatsApp, screenshots, and most re-saved/compressed images strip EXIF
# entirely). This is clearly flagged as sample data via "exif_is_sample"
# below rather than silently presented as if extracted from this file —
# a forensics tool mixing real and fabricated evidence without a label
# would undercut the whole chain-of-custody premise.
_SAMPLE_EXIF = {
    "Make": "Apple",
    "Model": "iPhone 13 Pro",
    "DateTimeOriginal": "2026:03:14 17:22:41",
    "Software": "iOS 17.4.1",
    "Orientation": "1 (top-left)",
    "ISOSpeedRatings": "100",
    "GPSInfo": "28.6139° N, 77.2090° E",
}


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

    exif_is_sample = False
    if not exif_data:
        exif_data = dict(_SAMPLE_EXIF)
        exif_is_sample = True

    return {
        "filename": filename,
        "width": img.width,
        "height": img.height,
        "format": img.format,
        "mode": img.mode,
        "size_bytes": len(data),
        "analyzed_at_utc": datetime.now(timezone.utc).isoformat(),
        "exif": exif_data,
        "exif_is_sample": exif_is_sample,
    }