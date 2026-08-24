"use client";

import { useCallback, useRef, useState } from "react";
import { analyzeImage, AnalyzeResponse, reportDownloadUrl } from "@/lib/api";
import EvidenceTag from "@/components/EvidenceTag";
import ScoreBar from "@/components/ScoreBar";
import PropagationTimeline from "@/components/PropagationTimeline";

type Tab = "assessment" | "metadata" | "timeline";

export default function Home() {
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [tab, setTab] = useState<Tab>("assessment");
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(async (file: File) => {
    setError(null);
    setData(null);
    setPreview(URL.createObjectURL(file));
    setLoading(true);
    try {
      const result = await analyzeImage(file);
      setData(result);
      setTab("assessment");
    } catch (e: any) {
      setError(e.message || "Something went wrong analyzing this file.");
    } finally {
      setLoading(false);
    }
  }, []);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <main className="min-h-screen">
      {/* Top bar */}
      <header className="border-b border-hairline bg-surface/60 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded border border-stamp/50 font-mono text-xs text-stamp">
              TT
            </div>
            <div>
              <h1 className="font-display text-lg font-semibold leading-none tracking-tight">
                TruthTrace AI
              </h1>
              <p className="text-[11px] uppercase tracking-[0.18em] text-muted">
                Chandigarh Police · Digital Forensics Unit
              </p>
            </div>
          </div>
          <span className="hidden font-mono text-xs text-muted sm:block">
            Detect · Verify · Trace
          </span>
        </div>
      </header>

      <div className="mx-auto grid max-w-6xl gap-8 px-6 py-10 lg:grid-cols-[380px_1fr]">
        {/* Left: upload + evidence tag */}
        <section className="space-y-6">
          <div
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => inputRef.current?.click()}
            className={`cursor-pointer rounded-lg border-2 border-dashed p-10 text-center transition-colors ${
              dragging ? "border-stamp bg-stamp/5" : "border-hairline bg-surface hover:border-muted"
            }`}
          >
            {preview ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={preview} alt="Uploaded evidence preview" className="mx-auto max-h-64 rounded shadow-lg" />
            ) : (
              <>
                <p className="font-display text-lg text-paper/90">Upload evidence</p>
                <p className="mt-2 text-sm text-muted">
                  Drag an image here, or click to browse.<br />JPG, PNG, WEBP supported.
                </p>
              </>
            )}
            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFile(file);
              }}
            />
          </div>

          {loading && (
            <div className="relative overflow-hidden rounded border border-hairline bg-surface p-4 text-sm text-muted">
              <div className="absolute inset-x-0 top-0 h-0.5 bg-stamp/60 animate-scanline" />
              Analyzing evidence — computing hash, running detector, reconstructing timeline…
            </div>
          )}

          {error && (
            <div className="rounded border border-danger/50 bg-danger/10 p-4 text-sm text-danger">
              {error}
            </div>
          )}

          {data && <EvidenceTag caseId={data.case_id} result={data.result} />}

          {data && (
            <a
              href={reportDownloadUrl(data.report_url)}
              className="block rounded border border-hairline bg-surface px-4 py-3 text-center text-sm font-medium text-paper hover:border-stamp hover:text-stamp transition-colors"
            >
              ⬇ Download forensic report (PDF)
            </a>
          )}
        </section>

        {/* Right: tabbed results */}
        <section className="rounded-lg border border-hairline bg-surface min-h-[420px]">
          {!data ? (
            <div className="flex h-full min-h-[420px] items-center justify-center px-8 text-center text-sm text-muted">
              Investigation results will appear here once evidence is analyzed.
            </div>
          ) : (
            <>
              <nav className="flex border-b border-hairline">
                {([
                  ["assessment", "Assessment"],
                  ["metadata", "Metadata"],
                  ["timeline", "Propagation"],
                ] as [Tab, string][]).map(([key, label]) => (
                  <button
                    key={key}
                    onClick={() => setTab(key)}
                    className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors ${
                      tab === key
                        ? "border-stamp text-stamp"
                        : "border-transparent text-muted hover:text-paper"
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </nav>

              <div className="p-6">
                {tab === "assessment" && (
                  <div>
                    <h2 className="font-display text-lg font-semibold mb-4">
                      Forensic Evidence Scorecard
                    </h2>
                    <ScoreBar
                      label="Model confidence"
                      value={data.result.confidence}
                      hint="Pretrained classifier output on the uploaded image"
                    />
                    <ScoreBar
                      label="EXIF fields recovered"
                      value={Object.keys(data.metadata.exif).length}
                      suffix=""
                      hint="More fields generally indicate less post-processing"
                    />
                    <ScoreBar
                      label="Cross-platform matches"
                      value={data.timeline.length}
                      suffix=""
                      hint="Simulated propagation hits for this demo"
                    />
                  </div>
                )}

                {tab === "metadata" && (
                  <div className="space-y-1 font-mono text-sm">
                    <Row k="Case ID" v={data.case_id} />
                    <Row k="SHA-256" v={data.hash} mono />
                    <Row k="Filename" v={data.metadata.filename} />
                    <Row k="Dimensions" v={`${data.metadata.width} × ${data.metadata.height}`} />
                    <Row k="Format" v={data.metadata.format} />
                    <Row k="Color mode" v={data.metadata.mode} />
                    <Row k="Size" v={`${data.metadata.size_bytes.toLocaleString()} bytes`} />
                    <Row k="Analyzed (UTC)" v={data.metadata.analyzed_at_utc} />
                  </div>
                )}

                {tab === "timeline" && <PropagationTimeline entries={data.timeline} />}
              </div>
            </>
          )}
        </section>
      </div>
    </main>
  );
}

function Row({ k, v, mono }: { k: string; v: string; mono?: boolean }) {
  return (
    <div className="flex justify-between gap-4 border-b border-hairline/60 py-2 last:border-0">
      <span className="text-muted">{k}</span>
      <span className={`text-right text-paper/90 break-all ${mono ? "text-xs" : ""}`}>{v}</span>
    </div>
  );
}
