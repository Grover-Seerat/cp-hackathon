import { TimelineEntry } from "@/lib/api";

export default function PropagationTimeline({ entries }: { entries: TimelineEntry[] }) {
  if (!entries.length) {
    return <p className="text-sm text-muted">No propagation data available for this case.</p>;
  }

  return (
    <div>
      <p className="mb-4 text-[11px] uppercase tracking-[0.15em] text-muted">
        Simulated for demo — wire to a reverse-image-search API in production
      </p>
      <ol className="relative border-l border-hairline pl-6">
        {entries.map((entry, i) => (
          <li key={i} className="mb-6 last:mb-0">
            <span className="absolute -left-[7px] mt-1 h-3 w-3 rounded-full bg-stamp ring-4 ring-ink" />
            <div className="flex items-baseline gap-3">
              <span className="font-mono text-sm text-stamp">{entry.time}</span>
              <span className="font-display text-base font-semibold text-paper">{entry.platform}</span>
            </div>
            {entry.note && <p className="mt-0.5 text-sm text-muted">{entry.note}</p>}
          </li>
        ))}
      </ol>
    </div>
  );
}
