import { AlertTriangle, RefreshCw, ShieldCheck, Clock } from "lucide-react";
import { inr } from "@/lib/api";

const stamp = (iso) => {
  const d = new Date(iso);
  return `${d.toLocaleDateString("en-IN", { day: "2-digit", month: "short" })} · ${d.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false })}`;
};

const Chip = ({ children }) => (
  <span className="font-mono text-[10px] px-2 py-0.5 rounded border border-[#232A3B] text-[#94A3B8]">{children}</span>
);

export const AuditLog = ({ entries, loading, onRefresh }) => {
  const flagCount = (entries || []).reduce((a, e) => a + (e.warnings?.length || 0), 0);
  return (
    <section data-testid="warning-audit-log" className="panel p-6 reveal">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="eyebrow">Zone 4 · Compliance audit trail</p>
          <h3 className="font-heading text-lg font-bold mt-1">Warning audit log</h3>
          <p className="text-sm text-[#94A3B8] mt-1">Every guardrail flag raised by the optimizer, timestamped and stored server-side for policy review.</p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span data-testid="audit-flag-total" className="font-mono text-[11px] px-3 py-1.5 rounded-full border border-[#232A3B] text-[#94A3B8]">{flagCount} flags · {entries?.length || 0} events</span>
          <button data-testid="audit-refresh-button" onClick={onRefresh} className="btn-ghost text-xs px-3 py-1.5 flex items-center gap-1.5">
            <RefreshCw size={12} className={loading ? "animate-spin" : ""} /> Refresh
          </button>
        </div>
      </div>

      {!entries ? (
        <div className="space-y-2 mt-6">{[1, 2, 3].map((i) => <div key={i} className="h-16 rounded-lg bg-[#181E2B] animate-pulse" />)}</div>
      ) : entries.length === 0 ? (
        <div data-testid="audit-log-empty" className="flex items-center gap-2 mt-8 text-sm text-[#10B981]"><ShieldCheck size={16} /> No policy flags recorded yet. Run a shock scenario to populate the trail.</div>
      ) : (
        <div className="mt-5 space-y-2.5">
          {entries.map((e, idx) => (
            <div key={`${e.created_at}-${idx}`} data-testid={`audit-entry-${idx}`} className="rounded-xl border border-[#232A3B] bg-[#11151E] p-4">
              <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
                <span data-testid={`audit-entry-time-${idx}`} className="font-mono text-[11px] text-[#E2B859] flex items-center gap-1.5"><Clock size={11} /> {stamp(e.created_at)}</span>
                <span className="font-kpi text-lg leading-none text-[#F8FAFC]">{inr(e.price)}</span>
                <Chip>demand {e.scenario?.demand_index}</Chip>
                <Chip>rooms left {e.scenario?.capacity_remaining_pct}%</Chip>
                <Chip>{e.scenario?.days_to_arrival}d out</Chip>
                <Chip>{e.scenario?.season}</Chip>
                <Chip>comp {inr(e.scenario?.competitor_price)}</Chip>
                {e.scenario?.event_flag && <Chip>event</Chip>}
                <span className="ml-auto font-mono text-[10px] text-[#64748B]">{e.warnings?.length} flag(s)</span>
              </div>
              <div className="mt-3 grid gap-2 md:grid-cols-2">
                {(e.warnings || []).map((w) => (
                  <div key={w.code} className="warning-flag p-2.5">
                    <p className="flex items-center gap-1.5 text-xs font-semibold amber-text"><AlertTriangle size={12} /> {w.code} · {w.title}</p>
                    <p className="text-[11px] text-[#CBD5E1] mt-1">{w.detail}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};
