import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, ReferenceDot, CartesianGrid } from "recharts";

export const PaceChart = ({ forecast, pace }) => {
  if (!forecast) return <div className="panel p-5 h-[220px] animate-pulse" />;
  const data = forecast.pace_curve;
  const ahead = pace ? pace.pace_index >= 1 : true;
  return (
    <section data-testid="booking-pace-chart" className="panel p-5 reveal">
      <div className="flex items-baseline justify-between">
        <div>
          <p className="eyebrow">Booking pace · pickup model</p>
          <h3 className="font-heading text-sm font-semibold mt-0.5">% rooms sold vs days out (exp. τ={forecast.pace_tau}d)</h3>
        </div>
        {pace && (
          <span data-testid="pace-index-badge" className={`font-mono text-[11px] px-2 py-0.5 rounded-full border ${ahead ? "border-[#10B981]/40 text-[#10B981]" : "border-[#F59E0B]/40 text-[#F59E0B]"}`}>
            pace index {pace.pace_index}× · {ahead ? "ahead" : "behind"}
          </span>
        )}
      </div>
      <div className="h-[150px] mt-3">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="paceGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#E2B859" stopOpacity={0.35} />
                <stop offset="100%" stopColor="#E2B859" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#232A3B" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="days_out" reversed tick={{ fill: "#64748B", fontSize: 10 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#64748B", fontSize: 10 }} axisLine={false} tickLine={false} domain={[0, 100]} />
            <Tooltip contentStyle={{ background: "#0B0E14", border: "1px solid #232A3B", borderRadius: 8, fontSize: 12 }} formatter={(v) => [`${v}%`, "expected sold"]} labelFormatter={(l) => `${l} days out`} />
            <Area dataKey="expected_pct" stroke="#E2B859" strokeWidth={2} fill="url(#paceGrad)" />
            {pace && <ReferenceDot x={pace.days_to_arrival % 2 === 0 ? pace.days_to_arrival : pace.days_to_arrival - 1} y={pace.actual_sold_pct} r={6} fill={ahead ? "#10B981" : "#F59E0B"} stroke="#080A0F" strokeWidth={2} />}
          </AreaChart>
        </ResponsiveContainer>
      </div>
      {pace && <p className="text-[11px] text-[#64748B] mt-1 font-mono">on-the-books {pace.actual_sold_pct}% vs expected {pace.expected_sold_pct}% at {pace.days_to_arrival} days out</p>}
    </section>
  );
};
