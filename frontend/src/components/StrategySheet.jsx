import { inr, pct } from "@/lib/api";

export const StrategySheet = ({ result, explanation, decision, overridePrice, hotel }) => {
  if (!result) return null;
  const { scenario: sc, optimization: o, simulation: s, simulation_current: cur } = result;
  const m = o.multipliers;
  return (
    <div data-testid="strategy-sheet" className="print-only print-sheet font-sans text-black p-8 max-w-[800px] mx-auto">
      <h1 className="text-2xl font-bold">{hotel?.name} · Pricing Strategy Sheet</h1>
      <p className="text-sm text-gray-600">Generated {new Date().toLocaleString("en-IN")} · Single room type · {hotel?.total_rooms} rooms · INR</p>
      <hr className="my-4" />
      <h2 className="font-bold mt-4">1. Scenario</h2>
      <p className="text-sm">Demand index {sc.demand_index} · Capacity remaining {sc.capacity_remaining_pct}% · {sc.days_to_arrival} days to arrival · Season {sc.season} · Competitor {inr(sc.competitor_price)} · Event {sc.event_flag ? "yes" : "no"} · Current price {inr(sc.current_price)}</p>
      <h2 className="font-bold mt-4">2. Recommendation</h2>
      <p className="text-3xl font-bold">{inr(o.recommended_price)} <span className="text-sm font-normal">({((o.recommended_price / sc.current_price - 1) * 100).toFixed(1)}% vs current)</span></p>
      <p className="text-sm">Decision: <b>{decision}</b>{overridePrice ? ` · manager override ${inr(overridePrice)}` : ""}</p>
      <p className="text-sm">Revenue P10/P50/P90: {inr(s.revenue_p10)} / {inr(s.revenue_p50)} / {inr(s.revenue_p90)} · Expected occupancy {pct(s.occupancy_final_mean)} · Conversion {pct(s.conversion_rate, 1)} · vs current P50 {inr(cur.revenue_p50)}</p>
      <h2 className="font-bold mt-4">3. Rules used</h2>
      <ul className="text-sm list-disc pl-5">{o.rules_used.map((r, i) => <li key={i}>{r}</li>)}</ul>
      <p className="text-sm mt-2 font-mono">{inr(m.base_rate)} × season {m.season} × demand {m.demand} × capacity {m.capacity} × competitor {m.competitor} × lead {m.lead_time} × event {m.event} = {inr(o.formula_price)}</p>
      <h2 className="font-bold mt-4">4. Policy warnings ({o.warnings.length})</h2>
      {o.warnings.length === 0 ? <p className="text-sm">None triggered.</p> : <ul className="text-sm list-disc pl-5">{o.warnings.map((w) => <li key={w.code}><b>{w.title}</b> — {w.detail} <i>{w.mitigation}</i></li>)}</ul>}
      <h2 className="font-bold mt-4">5. AI rationale ({explanation?.source || "pending"})</h2>
      {explanation ? (
        <div className="text-sm space-y-2">
          <p><b>Why this price:</b> {explanation.why_this_price}</p>
          <p><b>Key risks:</b></p><ul className="list-disc pl-5">{explanation.key_risks.map((r, i) => <li key={i}>{r}</li>)}</ul>
          <p><b>Alternative strategy:</b> {explanation.alternative_strategy}</p>
        </div>
      ) : <p className="text-sm">Not generated.</p>}
    </div>
  );
};
