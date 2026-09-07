import { useCallback, useEffect, useRef, useState } from "react";
import "@/App.css";
import { Toaster, toast } from "sonner";
import { getConfig, getForecast, getPace, recommend, explain, saveRun } from "@/lib/api";
import { Header } from "@/components/Header";
import { InputsPanel } from "@/components/InputsPanel";
import { HeroCard } from "@/components/HeroCard";
import { ForecastChart } from "@/components/ForecastChart";
import { PaceChart } from "@/components/PaceChart";
import { MultiplierBreakdown } from "@/components/MultiplierBreakdown";
import { MonteCarloCard } from "@/components/MonteCarloCard";
import { ComparisonTable } from "@/components/ComparisonTable";
import { WarningsBox } from "@/components/WarningsBox";
import { ExplanationCard } from "@/components/ExplanationCard";
import { PresenterMode, PRESENTER_STEPS } from "@/components/PresenterMode";
import { StrategySheet } from "@/components/StrategySheet";

const DEFAULT = { demand_index: 100, capacity_remaining_pct: 60, days_to_arrival: 14, season: "shoulder", competitor_price: 5200, event_flag: false, current_price: 5000 };
const STEP_SECONDS = 20;

function App() {
  const [config, setConfig] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [scenario, setScenario] = useState(DEFAULT);
  const [pace, setPace] = useState(null);
  const [activePreset, setActivePreset] = useState(null);
  const [result, setResult] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [explaining, setExplaining] = useState(false);
  const [decision, setDecision] = useState("draft");
  const [overridePrice, setOverridePrice] = useState(null);
  const [presenter, setPresenter] = useState({ active: false, step: 0, paused: false, secondsLeft: STEP_SECONDS });
  const runIdRef = useRef(0);

  useEffect(() => {
    getConfig().then(setConfig).catch(() => toast.error("Backend unreachable"));
    getForecast().then(setForecast).catch(() => {});
  }, []);

  useEffect(() => {
    const t = setTimeout(() => getPace(scenario).then(setPace).catch(() => {}), 200);
    return () => clearTimeout(t);
  }, [scenario]);

  const runRecommend = useCallback(async (sc) => {
    const id = ++runIdRef.current;
    setLoading(true); setExplanation(null); setDecision("draft"); setOverridePrice(null);
    try {
      const r = await recommend(sc);
      if (id !== runIdRef.current) return;
      setResult(r); setLoading(false);
      setExplaining(true);
      const e = await explain(sc, r.optimization, r.simulation).catch(() => { toast.error("Explanation unavailable"); return null; });
      if (id === runIdRef.current) setExplanation(e);
    } catch (err) {
      toast.error("Optimizer failed: " + (err?.message || "unknown"));
    } finally {
      if (id === runIdRef.current) { setLoading(false); setExplaining(false); }
    }
  }, []);

  const onPreset = (p) => { setActivePreset(p.id); setScenario(p.scenario); runRecommend(p.scenario); };
  const onChangeScenario = (fn) => { setActivePreset(null); setScenario(fn); };

  const onRegenerate = async () => {
    if (!result) return;
    setExplaining(true);
    try { setExplanation(await explain(scenario, result.optimization, result.simulation, true)); } finally { setExplaining(false); }
  };

  const persist = async (dec, price) => {
    await saveRun({ label: activePreset || "custom", scenario, optimization: result.optimization, simulation: result.simulation, explanation, decision: dec, override_price: price });
  };
  const onAccept = async () => { setDecision("accepted"); await persist("accepted", null); toast.success(`Accepted ₹${result.optimization.recommended_price.toLocaleString("en-IN")} — run saved`); };
  const onOverride = async () => {
    const v = window.prompt("Override price (₹)", result.optimization.recommended_price);
    if (!v) return;
    const price = Number(v);
    if (!price || price < 500) return toast.error("Invalid price");
    setDecision("overridden"); setOverridePrice(price);
    await persist("overridden", price);
    toast(`Overridden to ₹${price.toLocaleString("en-IN")} — logged`);
  };

  const startPresenter = () => {
    setPresenter({ active: true, step: 0, paused: false, secondsLeft: STEP_SECONDS });
    const p = config?.presets.find((x) => x.id === PRESENTER_STEPS[0].preset);
    if (p) onPreset(p);
  };
  const presenterNext = useCallback(() => {
    setPresenter((ps) => {
      const next = ps.step + 1;
      if (next >= PRESENTER_STEPS.length) return { ...ps, active: false };
      const p = config?.presets.find((x) => x.id === PRESENTER_STEPS[next].preset);
      if (p) setTimeout(() => onPreset(p), 0);
      return { ...ps, step: next, secondsLeft: STEP_SECONDS };
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [config]);

  useEffect(() => {
    if (!presenter.active || presenter.paused) return;
    const t = setInterval(() => {
      setPresenter((ps) => (ps.secondsLeft <= 1 ? ps : { ...ps, secondsLeft: ps.secondsLeft - 1 }));
    }, 1000);
    return () => clearInterval(t);
  }, [presenter.active, presenter.paused]);

  useEffect(() => {
    if (presenter.active && !presenter.paused && presenter.secondsLeft <= 1) presenterNext();
  }, [presenter.secondsLeft, presenter.active, presenter.paused, presenterNext]);

  const onReset = () => { setScenario(DEFAULT); setActivePreset(null); setResult(null); setExplanation(null); setDecision("draft"); setPresenter({ active: false, step: 0, paused: false, secondsLeft: STEP_SECONDS }); };

  return (
    <div className="App">
      <Toaster theme="dark" position="top-right" toastOptions={{ style: { background: "#11151E", border: "1px solid #232A3B", color: "#F8FAFC" } }} />
      <Header hotel={config?.hotel} onPresenter={startPresenter} onPrint={() => window.print()} onReset={onReset} presenterActive={presenter.active} />
      <main className="no-print p-5 grid grid-cols-12 gap-4 max-w-[1800px] mx-auto">
        <div className="col-span-12 lg:col-span-3">
          <InputsPanel scenario={scenario} setScenario={onChangeScenario} presets={config?.presets || []} activePreset={activePreset} onPreset={onPreset} onRecommend={() => runRecommend(scenario)} loading={loading} />
        </div>
        <div className="col-span-12 lg:col-span-6 space-y-4">
          <HeroCard result={result} scenario={scenario} onAccept={onAccept} onOverride={onOverride} decision={decision} />
          <MultiplierBreakdown optimization={result?.optimization} />
          <div className="grid grid-cols-2 gap-4">
            <ForecastChart forecast={forecast} scenario={scenario} />
            <PaceChart forecast={forecast} pace={pace} />
          </div>
          <MonteCarloCard simulation={result?.simulation} />
          <ComparisonTable result={result} />
        </div>
        <div className="col-span-12 lg:col-span-3 space-y-4 flex flex-col">
          <WarningsBox warnings={result?.optimization.warnings} />
          <ExplanationCard explanation={explanation} loading={explaining} onRegenerate={onRegenerate} hasResult={!!result} />
        </div>
      </main>
      <PresenterMode active={presenter.active} step={presenter.step} paused={presenter.paused} secondsLeft={presenter.secondsLeft}
        onNext={presenterNext} onStop={() => setPresenter((p) => ({ ...p, active: false }))} onTogglePause={() => setPresenter((p) => ({ ...p, paused: !p.paused }))} />
      <StrategySheet result={result} explanation={explanation} decision={decision} overridePrice={overridePrice} hotel={config?.hotel} />
    </div>
  );
}

export default App;
