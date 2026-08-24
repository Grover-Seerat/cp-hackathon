export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "/api/backend";

export interface DetectionResult {
  label: string;
  confidence: number;
  warning?: string;
}

export interface Metadata {
  filename: string;
  width: number;
  height: number;
  format: string;
  mode: string;
  size_bytes: number;
  analyzed_at_utc: string;
  exif: Record<string, string>;
}

export interface TimelineEntry {
  platform: string;
  time: string;
  note?: string;
}

export interface AnalyzeResponse {
  case_id: string;
  result: DetectionResult;
  metadata: Metadata;
  hash: string;
  timeline: TimelineEntry[];
  report_url: string;
}

export async function analyzeImage(file: File): Promise<AnalyzeResponse> {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    const detail = await res.json().catch(() => ({}));
    throw new Error(detail.detail || `Analysis failed (${res.status})`);
  }

  return res.json();
}

export function reportDownloadUrl(reportUrl: string): string {
  return `${API_BASE}${reportUrl}`;
}