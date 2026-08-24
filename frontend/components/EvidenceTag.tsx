import { DetectionResult } from "@/lib/api";

function isManipulated(label: string) {
  const l = label.toLowerCase();
  return l.includes("artificial") || l.includes("fake") || l.includes("ai");
}

export default function EvidenceTag({
  caseId,
  result,
}: {
  caseId: string;
  result: DetectionResult;
}) {
  const flagged = isManipulated(result.label);
  const verdict = flagged ? "MANIPULATED / AI-GENERATED" : "LIKELY AUTHENTIC";
  const ink = flagged ? "text-danger border-danger" : "text-safe border-safe";

  return (
    <div className="relative animate-stamp">
      {/* perforated stub edge */}
      <div
        className="absolute -left-3 top-3 bottom-3 w-3 border-l-2 border-dashed border-hairline"
        aria-hidden
      />
      <div
        className={`-rotate-2 border-2 ${ink} bg-surface2/80 px-5 py-4 max-w-sm shadow-[0_8px_30px_rgba(0,0,0,0.45)]`}
        style={{ fontFamily: "var(--font-mono)" }}
      >
        <div className="flex items-baseline justify-between gap-4">
          <span className="text-[10px] tracking-[0.2em] text-muted uppercase">Evidence Tag</span>
          <span className="text-[10px] tracking-[0.2em] text-muted uppercase">{caseId}</span>
        </div>
        <div className={`mt-2 text-xl font-bold tracking-wide ${ink.split(" ")[0]}`}>
          {verdict}
        </div>
        <div className="mt-1 text-sm text-paper/80">
          Confidence: <span className="font-semibold">{result.confidence}%</span>
        </div>
        {result.warning && (
          <div className="mt-2 text-[11px] text-stamp/90 leading-snug">
            ⚠ {result.warning}
          </div>
        )}
      </div>
    </div>
  );
}
