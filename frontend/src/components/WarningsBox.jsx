import { AlertTriangle, ShieldCheck } from "lucide-react";

export const WarningsBox = ({ warnings }) => (
  <section data-testid="ethical-policy-warnings-box" className="panel p-5 reveal">
    <div className="flex items-baseline justify-between">
      <p className="eyebrow">Zone 3 · Ethical & policy guardrails</p>
      <span className="font-mono text-[10px] text-[#64748B]">flag, not block</span>
    </div>
    {!warnings ? (
      <p className="text-sm text-[#64748B] mt-3">Run the optimizer to evaluate surge, cost-floor and fairness rules.</p>
    ) : warnings.length === 0 ? (
      <div data-testid="no-warnings" className="flex items-center gap-2 mt-3 text-sm text-[#10B981]"><ShieldCheck size={16} /> All policy checks passed.</div>
    ) : (
      <div className="space-y-2 mt-3">
        {warnings.map((w) => (
          <div key={w.code} data-testid={`warning-${w.code.toLowerCase()}`} className="warning-flag p-3">
            <p className="flex items-center gap-1.5 text-sm font-semibold amber-text"><AlertTriangle size={14} /> {w.title}</p>
            <p className="text-xs text-[#CBD5E1] mt-1">{w.detail}</p>
            <p className="text-[11px] text-[#F59E0B]/80 mt-1.5 font-mono">→ {w.mitigation}</p>
          </div>
        ))}
      </div>
    )}
  </section>
);
