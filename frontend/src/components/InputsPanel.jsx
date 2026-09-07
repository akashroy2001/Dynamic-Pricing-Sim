import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Zap, Sparkles } from "lucide-react";
import { inr } from "@/lib/api";

const Field = ({ label, value, testId, children }) => (
  <div className="space-y-2">
    <div className="flex items-center justify-between">
      <span className="text-xs text-[#94A3B8]">{label}</span>
      <span data-testid={`${testId}-value`} className="font-mono text-xs gold-text">{value}</span>
    </div>
    {children}
  </div>
);

export const InputsPanel = ({ scenario, setScenario, presets, activePreset, onPreset, onRecommend, loading }) => {
  const set = (k) => (v) => setScenario((s) => ({ ...s, [k]: Array.isArray(v) ? v[0] : v }));
  const seasons = ["peak", "shoulder", "off"];
  return (
    <aside data-testid="inputs-panel" className="panel p-5 space-y-6 reveal">
      <div>
        <p className="eyebrow">Zone 1 · Manager Panel</p>
        <h2 className="font-heading text-base font-semibold mt-1">Scenario Inputs</h2>
      </div>

      <div className="space-y-5">
        <Field label="Base demand index" value={scenario.demand_index} testId="base-demand-index-slider">
          <Slider data-testid="base-demand-index-slider" min={0} max={200} step={5} value={[scenario.demand_index]} onValueChange={set("demand_index")} />
        </Field>
        <Field label="Capacity remaining" value={`${scenario.capacity_remaining_pct}% · ${scenario.capacity_remaining_pct} rooms`} testId="capacity-remaining-slider">
          <Slider data-testid="capacity-remaining-slider" min={0} max={100} step={1} value={[scenario.capacity_remaining_pct]} onValueChange={set("capacity_remaining_pct")} />
        </Field>
        <Field label="Days to arrival" value={`${scenario.days_to_arrival} d`} testId="days-to-arrival-slider">
          <Slider data-testid="days-to-arrival-slider" min={1} max={90} step={1} value={[scenario.days_to_arrival]} onValueChange={set("days_to_arrival")} />
        </Field>
        <Field label="Competitor avg price" value={inr(scenario.competitor_price)} testId="competitor-price-slider">
          <Slider data-testid="competitor-price-slider" min={1000} max={15000} step={100} value={[scenario.competitor_price]} onValueChange={set("competitor_price")} />
        </Field>
        <Field label="Your current price" value={inr(scenario.current_price)} testId="current-price-slider">
          <Slider data-testid="current-price-slider" min={1000} max={15000} step={100} value={[scenario.current_price]} onValueChange={set("current_price")} />
        </Field>

        <div className="space-y-2">
          <span className="text-xs text-[#94A3B8]">Season</span>
          <div className="grid grid-cols-3 gap-1.5">
            {seasons.map((s) => (
              <button key={s} data-testid={`season-${s}-button`} className={`seg-btn capitalize ${scenario.season === s ? "active" : ""}`} onClick={() => set("season")(s)}>{s}</button>
            ))}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <span className="text-xs text-[#94A3B8] block">Event in town</span>
            <span className="text-[10px] text-[#64748B]">Adds +20% price & demand multiplier</span>
          </div>
          <Switch data-testid="event-flag-switch" checked={scenario.event_flag} onCheckedChange={set("event_flag")} className="data-[state=checked]:bg-[#E2B859]" />
        </div>
      </div>

      <button data-testid="recommend-price-button" onClick={onRecommend} disabled={loading} className="btn-gold w-full py-3 text-sm flex items-center justify-center gap-2">
        <Sparkles size={15} /> {loading ? "Optimizing…" : "Recommend Price"}
      </button>

      <div className="space-y-2">
        <p className="eyebrow flex items-center gap-1.5"><Zap size={11} /> Shock presets</p>
        {presets.map((p) => (
          <button key={p.id} data-testid={`shock-preset-${p.id}-button`} className={`shock-btn w-full px-3 py-2.5 ${activePreset === p.id ? "active" : ""}`} onClick={() => onPreset(p)}>
            <span className="block text-sm font-medium text-[#F8FAFC]">{p.name}</span>
            <span className="block text-[11px] text-[#64748B]">{p.tagline}</span>
          </button>
        ))}
      </div>
    </aside>
  );
};
