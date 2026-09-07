import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, ReferenceLine, Cell } from "recharts";
import { inr, pct } from "@/lib/api";

const Pill = ({ label, value, testId, tone }) => (
  <div data-testid={testId} className={`rounded-lg border px-3 py-2 ${tone}`}>
    <p className="eyebrow">{label}</p>
    <p className="font-kpi text-2xl font-bold leading-none mt-1">{value}</p>
  </div>
);

export const MonteCarloCard = ({ simulation: s }) => {
  if (!s) return null;
  return (
    <section data-testid="monte-carlo-revenue-histogram" className="panel p-5 reveal">
      <div className="flex items-baseline justify-between">
        <div>
          <p className="eyebrow">Customer-side simulation · {s.iterations} runs</p>
          <h3 className="font-heading text-sm font-semibold mt-0.5">Revenue distribution at {inr(s.price)} — a range, not a number</h3>
        </div>
        <span className="font-mono text-[11px] text-[#64748B]">Leisure: price-sensitive · Business: time-sensitive</span>
      </div>
      <div className="grid grid-cols-3 gap-2 mt-4">
        <Pill label="P10 · pessimistic" value={inr(s.revenue_p10)} testId="monte-carlo-p10-stat" tone="border-[#232A3B] bg-[#181E2B] text-[#94A3B8]" />
        <Pill label="P50 · median" value={inr(s.revenue_p50)} testId="monte-carlo-p50-stat" tone="border-[#E2B859]/40 bg-[#E2B859]/10 gold-text" />
        <Pill label="P90 · optimistic" value={inr(s.revenue_p90)} testId="monte-carlo-p90-stat" tone="border-[#10B981]/30 bg-[#10B981]/5 text-[#10B981]" />
      </div>
      <div className="h-[150px] mt-3">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={s.histogram} margin={{ top: 10, right: 10, left: -20, bottom: 0 }} barCategoryGap={2}>
            <XAxis dataKey="revenue" tick={{ fill: "#64748B", fontSize: 10 }} tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#64748B", fontSize: 10 }} axisLine={false} tickLine={false} />
            <Tooltip cursor={{ fill: "rgba(226,184,89,0.06)" }} contentStyle={{ background: "#0B0E14", border: "1px solid #232A3B", borderRadius: 8, fontSize: 12 }} formatter={(v) => [v, "runs"]} labelFormatter={(l) => inr(l)} />
            <Bar dataKey="count" radius={[3, 3, 0, 0]}>
              {s.histogram.map((h, i) => <Cell key={i} fill={h.revenue >= s.revenue_p10 && h.revenue <= s.revenue_p90 ? "#E2B859" : "#3A4152"} />)}
            </Bar>
            <ReferenceLine x={s.histogram.reduce((a, b) => Math.abs(b.revenue - s.revenue_p50) < Math.abs(a.revenue - s.revenue_p50) ? b : a).revenue} stroke="#F8FAFC" strokeDasharray="3 3" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="grid grid-cols-4 gap-3 mt-3 text-center">
        {[
          ["Conversion", pct(s.conversion_rate, 1), "sim-conversion"],
          ["Bookings", `${s.bookings_mean} (${s.bookings_p10}–${s.bookings_p90})`, "sim-bookings"],
          ["Final occupancy", pct(s.occupancy_final_mean), "sim-occupancy"],
          ["Leisure / Business", `${pct(s.segments.leisure.share)} / ${pct(s.segments.business.share)}`, "sim-segment-mix"],
        ].map(([l, v, id]) => (
          <div key={id} className="rounded-lg bg-[#181E2B] border border-[#232A3B] py-2">
            <p className="eyebrow">{l}</p>
            <p data-testid={id} className="font-mono text-sm mt-1">{v}</p>
          </div>
        ))}
      </div>
    </section>
  );
};
