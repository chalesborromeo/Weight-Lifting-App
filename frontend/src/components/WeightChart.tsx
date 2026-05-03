import type { BodyMetric } from "@/types";

type Props = {
  /** Metrics newest-first (as returned by the API). Will be sorted ascending internally. */
  metrics: BodyMetric[];
  /** Optional goal weight — drawn as a dashed reference line. */
  goalWeight?: number | null;
};

const VIEW_W = 400;
const VIEW_H = 160;
const PAD_X = 12;
const PAD_Y_TOP = 16;
const PAD_Y_BOTTOM = 24;

/**
 * SVG line chart of weight over time. No external deps.
 * Scales to container width; maintains its own aspect ratio.
 */
export function WeightChart({ metrics, goalWeight }: Props) {
  // Oldest first for left-to-right plotting
  const points = [...metrics].sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime(),
  );

  if (points.length < 2) {
    return (
      <div className="bg-card rounded-[20px] p-6 text-center text-sm text-muted-foreground">
        Log at least 2 measurements to see the trend.
      </div>
    );
  }

  const values = points.map((p) => p.weight);
  const mins = Math.min(...values, ...(goalWeight != null ? [goalWeight] : []));
  const maxs = Math.max(...values, ...(goalWeight != null ? [goalWeight] : []));
  // Pad the domain 10% on each side to avoid the line hugging the edges.
  const range = Math.max(maxs - mins, 1);
  const domainMin = mins - range * 0.1;
  const domainMax = maxs + range * 0.1;

  const xFor = (i: number) =>
    PAD_X + (i / (points.length - 1)) * (VIEW_W - PAD_X * 2);
  const yFor = (value: number) => {
    const innerH = VIEW_H - PAD_Y_TOP - PAD_Y_BOTTOM;
    const pct = (value - domainMin) / (domainMax - domainMin);
    return PAD_Y_TOP + (1 - pct) * innerH;
  };

  const linePath = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${xFor(i).toFixed(2)} ${yFor(p.weight).toFixed(2)}`)
    .join(" ");

  // Area fill path: line path + down to baseline + back to start
  const areaPath = [
    linePath,
    `L ${xFor(points.length - 1).toFixed(2)} ${VIEW_H - PAD_Y_BOTTOM}`,
    `L ${xFor(0).toFixed(2)} ${VIEW_H - PAD_Y_BOTTOM}`,
    "Z",
  ].join(" ");

  const firstLabel = new Date(points[0].date).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
  const lastLabel = new Date(points[points.length - 1].date).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });

  return (
    <div className="bg-card rounded-[20px] p-4">
      <div className="flex items-baseline justify-between mb-2">
        <h3 className="text-sm text-muted-foreground uppercase tracking-wide">Weight trend</h3>
        <span className="text-xs text-muted-foreground">{points.length} entries</span>
      </div>

      <svg
        viewBox={`0 0 ${VIEW_W} ${VIEW_H}`}
        preserveAspectRatio="none"
        className="w-full h-40"
        role="img"
        aria-label="Weight over time"
      >
        <defs>
          <linearGradient id="wc-gradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="currentColor" stopOpacity="0.35" />
            <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
          </linearGradient>
        </defs>

        {/* Goal reference line */}
        {goalWeight != null && goalWeight >= domainMin && goalWeight <= domainMax && (
          <>
            <line
              x1={PAD_X}
              y1={yFor(goalWeight)}
              x2={VIEW_W - PAD_X}
              y2={yFor(goalWeight)}
              stroke="currentColor"
              strokeOpacity="0.35"
              strokeWidth="1"
              strokeDasharray="4 4"
              className="text-emerald-400"
            />
            <text
              x={VIEW_W - PAD_X}
              y={yFor(goalWeight) - 4}
              textAnchor="end"
              className="fill-emerald-400"
              fontSize="10"
            >
              goal {goalWeight}
            </text>
          </>
        )}

        {/* Area + line in accent color */}
        <g className="text-accent">
          <path d={areaPath} fill="url(#wc-gradient)" />
          <path
            d={linePath}
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          {points.map((p, i) => (
            <circle
              key={p.id}
              cx={xFor(i)}
              cy={yFor(p.weight)}
              r={i === points.length - 1 ? 4 : 2.5}
              className={i === points.length - 1 ? "fill-accent" : "fill-accent"}
            />
          ))}
        </g>

        {/* X-axis labels */}
        <text x={PAD_X} y={VIEW_H - 6} className="fill-muted-foreground" fontSize="10">
          {firstLabel}
        </text>
        <text
          x={VIEW_W - PAD_X}
          y={VIEW_H - 6}
          textAnchor="end"
          className="fill-muted-foreground"
          fontSize="10"
        >
          {lastLabel}
        </text>
      </svg>
    </div>
  );
}
