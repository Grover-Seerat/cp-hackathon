export default function ScoreBar({
  label,
  value,
  suffix = "%",
  hint,
}: {
  label: string;
  value: number;
  suffix?: string;
  hint?: string;
}) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div className="py-2.5">
      <div className="flex items-baseline justify-between">
        <span className="text-sm text-paper/85">{label}</span>
        <span className="font-mono text-sm text-stamp">{value}{suffix}</span>
      </div>
      <div className="mt-1.5 h-1.5 w-full rounded-full bg-hairline overflow-hidden">
        <div
          className="h-full rounded-full bg-stamp/80"
          style={{ width: `${suffix === "%" ? pct : Math.min(100, pct * 8)}%` }}
        />
      </div>
      {hint && <div className="mt-1 text-[11px] text-muted">{hint}</div>}
    </div>
  );
}
