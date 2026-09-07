import { inr } from "@/lib/api";

const LABELS = { season: "Season", demand: "Demand", capacity: "Capacity scarcity", competitor: "Competitor adj.", lead_time: "Lead time", event: "Event surge" };

export const MultiplierBreakdown = ({ optimization }) => {
  if (!optimization) return null;
  const m = optimization.multipliers;
  return (
    <section data-testid="multiplier-breakdown" className="panel p-5 reveal">
      <p className="eyebrow">Rule-based optimizer · multiplier chain</p>
      <div className="flex items-center flex-wrap gap-2 mt-3 font-mono text-xs">
        <span className="px-2.5 py-1.5 rounded-md bg-[#181E2B] border border-[#232A3B]">Base {inr(m.base_rate)}</span>
        {Object.keys(LABELS).map((k) => {
          const v = m[k];
          const tone = v > 1.001 ? "text-[#10B981] border-[#10B981]/30" : v < 0.999 ? "text-[#06B6D4] border-[#06B6D4]/30" : "text-[#64748B] border-[#232A3B]";
          return (
            <span key={k} className="flex items-center gap-2">
              <span className="text-[#64748B]">×</span>
              <span data-testid={`mult-${k}`} className={`px-2.5 py-1.5 rounded-md bg-[#181E2B] border ${tone}`} title={LABELS[k]}>
                <span className="text-[#94A3B8] mr-1.5">{LABELS[k]}</span>{v.toFixed(2)}
              </span>
            </span>
          );
        })}
        <span className="text-[#64748B]">=</span>
        <span data-testid="formula-price-value" className="px-2.5 py-1.5 rounded-md bg-[#E2B859]/10 border border-[#E2B859]/40 gold-text font-semibold">{inr(optimization.formula_price)}</span>
        <span className="text-[#64748B]">→ revenue max →</span>
        <span className="px-2.5 py-1.5 rounded-md bg-[#E2B859] text-[#0B0E14] font-bold">{inr(optimization.recommended_price)}</span>
      </div>
    </section>
  );
};
