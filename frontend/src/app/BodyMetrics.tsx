import { useEffect, useMemo, useState } from "react";
import { Plus, TrendingDown, TrendingUp, Minus } from "lucide-react";
import { bodyMetricsApi } from "@/api";
import { SectionHeader } from "@/components/SectionHeader";
import type { BodyMetric, BodyMetricCreate } from "@/types";

export default function BodyMetrics() {
  const [metrics, setMetrics] = useState<BodyMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      setMetrics(await bodyMetricsApi.list());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load metrics");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const latest = metrics[0]; // backend returns date desc
  const previous = metrics[1];

  const trend = useMemo(() => {
    if (!latest || !previous) return null;
    const delta = latest.weight - previous.weight;
    if (Math.abs(delta) < 0.05) return { delta: 0, direction: "flat" as const };
    return { delta, direction: delta > 0 ? ("up" as const) : ("down" as const) };
  }, [latest, previous]);

  const handleCreated = (m: BodyMetric) => {
    setMetrics((prev) => [m, ...prev]);
    setShowForm(false);
  };

  return (
    <div className="space-y-6">
      <SectionHeader title="Body Metrics" />

      {/* Hero card of latest */}
      {latest ? (
        <div className="bg-card rounded-[20px] p-6">
          <div className="flex items-baseline justify-between mb-4">
            <span className="text-xs text-muted-foreground uppercase tracking-wide">
              Latest · {new Date(latest.date).toLocaleDateString()}
            </span>
            {trend && <TrendBadge delta={trend.delta} direction={trend.direction} />}
          </div>
          <div className="grid grid-cols-3 gap-4">
            <Stat label="Weight" value={fmt(latest.weight)} unit="lbs" />
            <Stat label="Height" value={fmt(latest.height)} unit="in" />
            <Stat label="Body Fat" value={fmt(latest.body_fat_pct)} unit="%" />
          </div>
        </div>
      ) : (
        !loading && (
          <div className="bg-card rounded-[20px] p-8 text-center text-sm text-muted-foreground">
            No measurements yet. Log your first below.
          </div>
        )
      )}

      <button
        onClick={() => setShowForm((v) => !v)}
        className="w-full flex items-center justify-center gap-2 bg-accent text-white px-4 py-3 rounded-[15px] active:scale-95 transition-transform"
      >
        <Plus className="w-4 h-4" />
        {showForm ? "Cancel" : "Log measurement"}
      </button>

      {showForm && <AddForm onCreated={handleCreated} />}

      {loading && <div className="text-sm text-muted-foreground">Loading...</div>}
      {error && <div className="text-sm text-destructive">{error}</div>}

      {metrics.length > 1 && (
        <div className="space-y-3">
          <h2 className="text-sm uppercase tracking-wide text-muted-foreground">History</h2>
          {metrics.slice(1).map((m) => (
            <HistoryRow key={m.id} metric={m} />
          ))}
        </div>
      )}
    </div>
  );
}

function fmt(n: number | null | undefined): string {
  if (n === null || n === undefined) return "—";
  return n % 1 === 0 ? String(n) : n.toFixed(1);
}

function Stat({ label, value, unit }: { label: string; value: string; unit: string }) {
  return (
    <div>
      <div className="text-xs text-muted-foreground">{label}</div>
      <div className="mt-1 text-2xl font-semibold text-foreground">
        {value}
        <span className="ml-1 text-sm font-normal text-muted-foreground">{unit}</span>
      </div>
    </div>
  );
}

function TrendBadge({ delta, direction }: { delta: number; direction: "up" | "down" | "flat" }) {
  const Icon = direction === "up" ? TrendingUp : direction === "down" ? TrendingDown : Minus;
  const color =
    direction === "up"
      ? "text-amber-400"
      : direction === "down"
      ? "text-emerald-400"
      : "text-muted-foreground";
  return (
    <span className={`flex items-center gap-1 text-xs ${color}`}>
      <Icon className="w-3.5 h-3.5" />
      {delta === 0 ? "no change" : `${delta > 0 ? "+" : ""}${delta.toFixed(1)} lbs`}
    </span>
  );
}

function HistoryRow({ metric }: { metric: BodyMetric }) {
  return (
    <div className="bg-card rounded-[20px] p-4 flex items-center justify-between">
      <div className="text-sm text-muted-foreground">
        {new Date(metric.date).toLocaleDateString()}
      </div>
      <div className="flex gap-4 text-sm">
        <span className="text-foreground">
          <strong>{fmt(metric.weight)}</strong> lbs
        </span>
        {metric.height != null && (
          <span className="text-muted-foreground">{fmt(metric.height)} in</span>
        )}
        {metric.body_fat_pct != null && (
          <span className="text-muted-foreground">{fmt(metric.body_fat_pct)}%</span>
        )}
      </div>
    </div>
  );
}

function AddForm({ onCreated }: { onCreated: (m: BodyMetric) => void }) {
  const [weight, setWeight] = useState("");
  const [height, setHeight] = useState("");
  const [bodyFat, setBodyFat] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = weight.trim().length > 0 && !submitting;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    setSubmitting(true);
    setError(null);
    try {
      const body: BodyMetricCreate = {
        weight: Number(weight),
        height: height ? Number(height) : null,
        body_fat_pct: bodyFat ? Number(bodyFat) : null,
      };
      const created = await bodyMetricsApi.create(body);
      setWeight("");
      setHeight("");
      setBodyFat("");
      onCreated(created);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-card rounded-[20px] p-4 space-y-3">
      <NumberField label="Weight (lbs)" value={weight} onChange={setWeight} autoFocus required />
      <NumberField label="Height (in)" value={height} onChange={setHeight} />
      <NumberField label="Body Fat (%)" value={bodyFat} onChange={setBodyFat} />
      {error && <div className="text-sm text-destructive">{error}</div>}
      <button
        type="submit"
        disabled={!canSubmit}
        className={`w-full px-4 py-3 rounded-[12px] transition-all ${
          canSubmit
            ? "bg-accent text-white active:scale-95"
            : "bg-inactive text-muted-foreground cursor-not-allowed"
        }`}
      >
        {submitting ? "Saving..." : "Save measurement"}
      </button>
    </form>
  );
}

function NumberField({
  label,
  value,
  onChange,
  required,
  autoFocus,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  required?: boolean;
  autoFocus?: boolean;
}) {
  return (
    <label className="flex items-center justify-between px-2 py-1">
      <span className="text-sm text-foreground">
        {label}
        {required && <span className="text-destructive ml-1">*</span>}
      </span>
      <input
        type="number"
        inputMode="decimal"
        step="any"
        min="0"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
        autoFocus={autoFocus}
        className="w-28 px-3 py-2 bg-background rounded-[10px] text-foreground text-right outline-none focus:ring-2 focus:ring-accent/30"
      />
    </label>
  );
}
