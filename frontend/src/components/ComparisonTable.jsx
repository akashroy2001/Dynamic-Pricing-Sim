import { inr, pct } from "@/lib/api";

const Delta = ({ v, fmt, testId }) => (
  <span data-testid={testId} className={`font-mono text-[11px] ${v > 0 ? "text-[#10B981]" : v < 0 ? "text-[#06B6D4]" : "text-[#64748B]"}`}>{v > 0 ? "+" : ""}{fmt(v)}</span>
);

export const ComparisonTable = ({ result }) => {
  if (!result) return null;
  const { simulation: rec, simulation_current: cur, simulation_competitor: comp, scenario } = result;
  const spread = (s) => s.revenue_p90 - s.revenue_p10;
  const cols = [
    { key: "current", label: "Current price", sim: cur, price: scenario.current_price, tone: "" },
    { key: "recommended", label: "Recommended", sim: rec, price: rec.price, tone: "bg-[#E2B859]/10 border-x border-[#E2B859]/30" },
    { key: "competitor", label: "Match competitor", sim: comp, price: scenario.competitor_price, tone: "" },
  ];
  const rows = [
    ["Rate", (c) => inr(c.price), null],
    ["Revenue P50", (c) => inr(c.sim.revenue_p50), (c) => <Delta v={c.sim.revenue_p50 - cur.revenue_p50} fmt={inr} testId={`cmp-${c.key}-revenue-delta`} />],
    ["Occupancy", (c) => pct(c.sim.occupancy_final_mean), (c) => <Delta v={(c.sim.occupancy_final_mean - cur.occupancy_final_mean) * 100} fmt={(v) => `${v.toFixed(1)} pts`} testId={`cmp-${c.key}-occ-delta`} />],
    ["Risk (P90−P10 spread)", (c) => inr(spread(c.sim)), (c) => <Delta v={spread(c.sim) - spread(cur)} fmt={inr} testId={`cmp-${c.key}-risk-delta`} />],
    ["Sell-out probability", (c) => pct(c.sim.sellout_probability), null],
  ];
  return (
    <section data-testid="rate-comparison-table" className="panel p-5 reveal">
      <p className="eyebrow">Comparison view · vs current</p>
      <table className="w-full mt-3 text-sm">
        <thead>
          <tr className="text-left">
            <th className="py-2 text-[#64748B] font-normal text-xs"></th>
            {cols.map((c) => <th key={c.key} className={`py-2 px-3 font-heading font-semibold text-xs ${c.key === "recommended" ? "gold-text" : "text-[#94A3B8]"} ${c.tone}`}>{c.label}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map(([label, val, delta]) => (
            <tr key={label} className="border-t border-[#232A3B]">
              <td className="py-2.5 text-xs text-[#94A3B8]">{label}</td>
              {cols.map((c) => (
                <td key={c.key} className={`py-2.5 px-3 ${c.tone}`}>
                  <span className={`font-mono ${c.key === "recommended" ? "text-[#F8FAFC] font-semibold" : ""}`}>{val(c)}</span>
                  {delta && c.key !== "current" && <span className="ml-2">{delta(c)}</span>}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};
