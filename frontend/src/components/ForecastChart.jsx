import { Area, ComposedChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, ReferenceLine, ReferenceDot } from "recharts";

const Tip = ({ active, payload, label }) => active && payload?.length ? (
  <div className="custom-tooltip">
    <p className="text-[#94A3B8]">{label}</p>
    {payload.filter((p) => p.dataKey !== "band").map((p) => <p key={p.dataKey} style={{ color: p.color }}>{p.name}: {typeof p.value === "number" ? p.value.toFixed(1) : p.value}</p>)}
  </div>
) : null;

export const ForecastChart = ({ forecast, scenario }) => {
  if (!forecast) return <div className="panel p-5 h-[260px] animate-pulse" />;
  const data = forecast.next_14_days.map((d) => ({ ...d, label: `${d.day} ${d.date.slice(8)}`, band: [d.low, d.high] }));
  const idx = Math.min(scenario.days_to_arrival, 14) - 1;
  const target = data[idx];
  return (
    <section data-testid="demand-forecast-line-chart" className="panel p-5 reveal">
      <div className="flex items-baseline justify-between">
        <div>
          <p className="eyebrow">Forecast · next 14 days</p>
          <h3 className="font-heading text-sm font-semibold mt-0.5">Demand index (seasonality + weekday + noise, seeded)</h3>
        </div>
        <span className="font-mono text-[11px] text-[#64748B]">365-day synthetic curve · seed 42</span>
      </div>
      <div className="h-[200px] mt-3">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="bandGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#06B6D4" stopOpacity={0.25} />
                <stop offset="100%" stopColor="#06B6D4" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#232A3B" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="label" tick={{ fill: "#64748B", fontSize: 10 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#64748B", fontSize: 10 }} axisLine={false} tickLine={false} domain={["dataMin - 10", "dataMax + 10"]} tickFormatter={(v) => Math.round(v)} />
            <Tooltip content={<Tip />} />
            <Area dataKey="band" name="80% band" fill="url(#bandGrad)" stroke="none" />
            <Line dataKey="forecast" name="Forecast" stroke="#E2B859" strokeWidth={2.5} dot={false} />
            <ReferenceLine y={100} stroke="#64748B" strokeDasharray="4 4" label={{ value: "baseline 100", fill: "#64748B", fontSize: 10, position: "insideTopRight" }} />
            {target && <ReferenceDot x={target.label} y={target.forecast} r={5} fill="#E2B859" stroke="#080A0F" strokeWidth={2} />}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
};
