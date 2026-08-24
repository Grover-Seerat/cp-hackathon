"""
app.py
TruthTrace AI backend — FastAPI service.

Endpoints:
  POST /analyze         -> upload image, get detection + evidence + report link
  GET  /report/{name}   -> download the generated PDF
  GET  /timeline         -> sample propagation timeline (simulated for demo)
  GET  /cases            -> audit log of every analysis run this session
  GET  /health            -> simple healthcheck
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
import os
import sqlite3
from datetime import datetime, timezone

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from detector import detect_image
from report import create_pdf, REPORTS_DIR
from utils import generate_hash, generate_case_id, extract_metadata

app = FastAPI(title="TruthTrace AI", version="0.1.0")

from detector import detect_image
from report import create_pdf, REPORTS_DIR
from utils import generate_hash, generate_case_id, extract_metadata

app = FastAPI(title="TruthTrace AI", version="0.1.0")

# Allow the Next.js dev server (default port 3000) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(title="TruthTrace AI", version="0.1.0")
DB_PATH = os.path.join("/tmp", "truthtrace.db")
# DB_PATH = os.path.join(os.path.dirname(__file__), "truthtrace.db")
SAMPLE_TIMELINE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "sample_data", "timeline.json"
)


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS evidence_log (
            case_id TEXT PRIMARY KEY,
            filename TEXT,
            sha256 TEXT,
            label TEXT,
            confidence REAL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


_init_db()


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/analyze")
async def analyze(file: UploadFile):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    case_id = generate_case_id()
    sha256 = generate_hash(image_bytes)
    metadata = extract_metadata(image_bytes, file.filename or "upload")
    result = detect_image(image_bytes)

    # Simulated cross-platform spread (see sample_data/timeline.json)
    try:
        with open(SAMPLE_TIMELINE_PATH) as f:
            timeline = json.load(f)
    except FileNotFoundError:
        timeline = []

    report_filename = create_pdf(case_id, result, metadata, sha256, timeline)

    # Append to the evidence / chain-of-custody log
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO evidence_log VALUES (?, ?, ?, ?, ?, ?)",
        (case_id, metadata["filename"], sha256, result["label"], result["confidence"],
         metadata["analyzed_at_utc"]),
    )
    conn.commit()
    conn.close()

    return {
        "case_id": case_id,
        "result": result,
        "metadata": metadata,
        "hash": sha256,
        "timeline": timeline,
        "report_url": f"/report/{report_filename}",
    }


@app.get("/report/{filename}")
def get_report(filename: str):
    filepath = os.path.join(REPORTS_DIR, filename)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="Report not found.")
    return FileResponse(filepath, media_type="application/pdf", filename=filename)


@app.get("/timeline")
def get_sample_timeline():
    try:
        with open(SAMPLE_TIMELINE_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


@app.get("/cases")
def list_cases():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM evidence_log ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
