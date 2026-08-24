# TruthTrace AI

**Detect. Verify. Trace.**
A digital forensics MVP for Chandigarh Police (Hackathon PS4): upload an image, get an AI authenticity verdict, forensic evidence (hash + metadata), a reconstructed spread timeline, and a downloadable PDF report.

This is a working starter kit, not a mockup — the upload → detect → hash → report flow actually runs end to end. The social-media propagation timeline is simulated with sample data (clearly labeled as such in the UI) rather than live scraping, per the hackathon-scope plan.

## Stack

| Layer      | Technology                                      |
|------------|--------------------------------------------------|
| Frontend   | Next.js 14 (App Router) + TypeScript + Tailwind   |
| Backend    | FastAPI                                           |
| AI         | Hugging Face `umm-maybe/AI-image-detector` (pretrained, no training needed) |
| Database   | SQLite (evidence/audit log)                       |
| Reports    | ReportLab (PDF)                                   |

## Quick start

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # optional, see DEMO_MODE below
uvicorn app:app --reload
```

Backend runs at `http://localhost:8000`. Check `http://localhost:8000/health`.

**First run downloads the Hugging Face model** (a few hundred MB) — do this before your demo, not during it, in case of slow venue wifi.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Frontend runs at `http://localhost:3000`.

### 3. Demo it

1. Open `http://localhost:3000`.
2. Drag in a test image (see `sample_data/` for suggestions — add your own AI-generated / real test images before the demo).
3. Watch the evidence tag stamp in with a verdict + confidence.
4. Check the **Metadata** tab for the SHA-256 hash and EXIF data.
5. Check the **Propagation** tab for the reconstructed spread timeline.
6. Click **Download forensic report** for the PDF.

## Demo-safety net: `DEMO_MODE`

Live model inference can fail on bad wifi or a cold Hugging Face download. Set `DEMO_MODE=1` in `backend/.env` (or `export DEMO_MODE=1`) to skip the real model and use deterministic, plausible-looking results instead — same image always gives the same verdict, so your rehearsed demo script stays consistent. Turn it back to `0` for the real thing.

## What's real vs. simulated (be upfront with judges about this)

| Feature                     | Status                                             |
|------------------------------|-----------------------------------------------------|
| Image upload & analysis      | Real — actual HTTP call, real inference             |
| AI authenticity detection    | Real — pretrained Hugging Face classifier           |
| SHA-256 hash / metadata/EXIF | Real — computed from the actual uploaded bytes      |
| PDF forensic report          | Real — generated per case, downloadable             |
| Evidence/audit log (SQLite)  | Real — every analysis is logged (`GET /cases`)      |
| Propagation timeline         | **Simulated** — sample JSON, not live scraping      |
| Manipulation heatmap         | Not built in this starter kit (see "Next steps")    |

Being explicit about this in your pitch ("here's what's live, here's what we'd wire up with a reverse-image-search API given more time") tends to land better with judges than implying everything is fully live.

## Project structure

```
truthtrace-ai/
├── backend/
│   ├── app.py          # FastAPI routes
│   ├── detector.py      # HF model wrapper + demo-mode fallback
│   ├── utils.py          # hashing, case IDs, EXIF/metadata extraction
│   ├── report.py          # PDF generation
│   └── requirements.txt
├── frontend/
│   ├── app/                # Next.js App Router pages
│   ├── components/          # EvidenceTag, ScoreBar, PropagationTimeline
│   └── lib/api.ts             # backend client
└── sample_data/
    └── timeline.json           # simulated propagation data
```

## API reference

| Method | Route              | Description                              |
|--------|---------------------|-------------------------------------------|
| POST   | `/analyze`            | Upload an image, get full analysis        |
| GET    | `/report/{filename}`   | Download a generated PDF report            |
| GET    | `/timeline`              | Sample propagation data                    |
| GET    | `/cases`                  | Evidence/audit log of past analyses        |
| GET    | `/health`                   | Healthcheck                                |

## Next steps (post-hackathon roadmap)

- Manipulation heatmap (face-region localization via InsightFace + Grad-CAM style overlay)
- Real reverse-image search (e.g. an image-search API) to replace the simulated timeline
- FAISS-based similarity search across a case database
- Auth + role-based access for investigators
- Chain-of-custody export (signed JSON alongside the PDF)
