import { useEffect, useState } from "react";
import { inr, lakhs, pct } from "@/lib/api";
import { ArrowUpRight, ArrowDownRight, Check, PencilLine } from "lucide-react";

const Big = ({ label, value, sub, testId, accent }) => (
  <div>
    <p className="eyebrow">{label}</p>
    <p data-testid={testId} className={`font-kpi font-bold text-5xl lg:text-6xl leading-none mt-1 ${accent || ""}`}>{value}</p>
    {sub && <p className="text-xs text-[#94A3B8] mt-1.5">{sub}</p>}
  </div>
);

export const HeroCard = ({ result, scenario, onAccept, onOverride, decision }) => {
  const [flash, setFlash] = useState(false);
  useEffect(() => { if (result) { setFlash(true); const t = setTimeout(() => setFlash(false), 700); return () => clearTimeout(t); } }, [result]);

  if (!result) {
    return (
      <section data-testid="recommended-price-hero-card" className="panel panel-elevated p-6 min-h-[190px] flex flex-col justify-center reveal">
        <p className="eyebrow">Zone 2 · Optimizer</p>
        <p className="font-heading text-2xl font-semibold mt-2 text-[#94A3B8]">Set the scenario, then hit <span className="gold-text">Recommend Price</span>.</p>
        <p className="text-sm text-[#64748B] mt-2">Baseline: 100 rooms · base rate {inr(5000)} · current price {inr(scenario.current_price)}</p>
      </section>
    );
  }
  const { optimization: o, simulation: s } = result;
  const price = o.recommended_price;
  const change = price / scenario.current_price - 1;
  const up = change >= 0;
  return (
    <section data-testid="recommended-price-hero-card" className="panel panel-elevated p-6 reveal overflow-hidden">
      <div className="absolute -right-16 -top-16 w-56 h-56 rounded-full bg-[#E2B859]/10 blur-3xl pointer-events-none" />
      <div className="flex items-start justify-between gap-6 flex-wrap">
        <div>
          <div className="flex items-center gap-3">
            <p className="eyebrow">Recommended rate · tonight</p>
            <span data-testid="price-change-badge" className={`font-mono text-[11px] px-2 py-0.5 rounded-full border ${up ? "border-[#10B981]/40 text-[#10B981]" : "border-[#06B6D4]/40 text-[#06B6D4]"} flex items-center gap-1`}>
              {up ? <ArrowUpRight size={11} /> : <ArrowDownRight size={11} />}{(change * 100).toFixed(1)}% vs current
            </span>
          </div>
          <p data-testid="recommended-price-value-text" className={`font-kpi font-extrabold gold-text text-7xl lg:text-8xl leading-none mt-1 ${flash ? "count-flash" : ""}`}>{inr(price)}</p>
          <p className="text-xs text-[#94A3B8] mt-2 font-mono">formula {inr(o.formula_price)} → optimized within ±30% · bounds {inr(o.price_bounds.floor)}–{inr(o.price_bounds.ceiling)}</p>
        </div>
        <div className="flex gap-8 flex-wrap">
          <Big label="Revenue P50" value={lakhs(s.revenue_p50)} sub={`${inr(s.revenue_p10)} – ${inr(s.revenue_p90)} (P10–P90)`} testId="hero-revenue-p50" />
          <Big label="Expected occupancy" value={pct(s.occupancy_final_mean)} sub={`${s.bookings_mean} of ${s.rooms_remaining} remaining rooms`} testId="hero-occupancy" accent="text-[#F8FAFC]" />
        </div>
      </div>
      <div className="flex items-center gap-2 mt-5 flex-wrap">
        <button data-testid="accept-price-button" onClick={onAccept} className={`btn-gold text-xs px-4 py-2 flex items-center gap-1.5 ${decision === "accepted" ? "ring-2 ring-[#10B981]" : ""}`}><Check size={13} /> {decision === "accepted" ? "Accepted" : "Accept price"}</button>
        <button data-testid="override-price-button" onClick={onOverride} className="btn-ghost text-xs px-4 py-2 flex items-center gap-1.5"><PencilLine size={13} /> Override</button>
        {o.constraint_binding && <span className="text-[11px] amber-text font-mono ml-2">occupancy target relaxed — infeasible at these inputs</span>}
        <span className="text-[11px] text-[#64748B] font-mono ml-auto">{s.iterations} Monte Carlo iterations · sell-out prob {pct(s.sellout_probability)}</span>
      </div>
    </section>
  );
};
