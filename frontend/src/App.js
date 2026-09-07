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
import { Zone } from "@/components/Zone";
import { AuditLog } from "@/components/AuditLog";
import { getWarningLog } from "@/lib/api";
import { ShieldAlert, LayoutDashboard } from "lucide-react";

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
  const [spotlight, setSpotlight] = useState(null);
  const [view, setView] = useState("dashboard");
  const [auditLog, setAuditLog] = useState(null);
  const [auditLoading, setAuditLoading] = useState(false);
  const runIdRef = useRef(0);

  const loadAudit = useCallback(async () => {
    setAuditLoading(true);
    try { setAuditLog(await getWarningLog()); } catch { setAuditLog([]); } finally { setAuditLoading(false); }
  }, []);

  useEffect(() => { loadAudit(); }, [loadAudit]);

  useEffect(() => {
    if (!spotlight) return;
    const el = document.querySelector(`[data-testid="zone-${spotlight}"]`);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
  }, [spotlight]);

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
      if (r.optimization.warnings?.length) loadAudit();
      setExplaining(true);
      const e = await explain(sc, r.optimization, r.simulation).catch(() => { toast.error("Explanation unavailable"); return null; });
      if (id === runIdRef.current) setExplanation(e);
    } catch (err) {
      toast.error("Optimizer failed: " + (err?.message || "unknown"));
    } finally {
      if (id === runIdRef.current) { setLoading(false); setExplaining(false); }
    }
  }, [loadAudit]);

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
    setView("dashboard");
    setPresenter({ active: true, step: 0, paused: false, secondsLeft: STEP_SECONDS });
    setSpotlight(PRESENTER_STEPS[0].zone);
    const p = config?.presets.find((x) => x.id === PRESENTER_STEPS[0].preset);
    if (p) onPreset(p);
  };
  const presenterNext = useCallback(() => {
    setPresenter((ps) => {
      const next = ps.step + 1;
      if (next >= PRESENTER_STEPS.length) { setTimeout(() => setSpotlight(null), 0); return { ...ps, active: false }; }
      const p = config?.presets.find((x) => x.id === PRESENTER_STEPS[next].preset);
      if (p) setTimeout(() => onPreset(p), 0);
      setTimeout(() => setSpotlight(PRESENTER_STEPS[next].zone), 0);
      return { ...ps, step: next, secondsLeft: STEP_SECONDS };
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [config]);

  const stopPresenter = () => { setPresenter((p) => ({ ...p, active: false })); setSpotlight(null); };

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

  const onReset = () => { setScenario(DEFAULT); setActivePreset(null); setResult(null); setExplanation(null); setDecision("draft"); setSpotlight(null); setView("dashboard"); setPresenter({ active: false, step: 0, paused: false, secondsLeft: STEP_SECONDS }); };

  const zoneProps = { spotlight, onSpotlight: setSpotlight, enabled: presenter.active };
  const auditFlags = (auditLog || []).reduce((a, e) => a + (e.warnings?.length || 0), 0);

  return (
    <div className="App">
      <Toaster theme="dark" position="top-right" toastOptions={{ style: { background: "#11151E", border: "1px solid #232A3B", color: "#F8FAFC" } }} />
      <Header hotel={config?.hotel} onPresenter={startPresenter} onPrint={() => window.print()} onReset={onReset} presenterActive={presenter.active} />

      <nav className="no-print px-6 border-b border-[#232A3B] flex items-center gap-6 bg-[#0B0E14]">
        <button data-testid="tab-dashboard" onClick={() => setView("dashboard")} className={`tab-btn text-sm font-semibold py-3 flex items-center gap-2 ${view === "dashboard" ? "active" : ""}`}>
          <LayoutDashboard size={14} /> Pricing dashboard
        </button>
        <button data-testid="tab-audit-log" onClick={() => { setView("audit"); loadAudit(); }} className={`tab-btn text-sm font-semibold py-3 flex items-center gap-2 ${view === "audit" ? "active" : ""}`}>
          <ShieldAlert size={14} /> Warning audit log
          {auditFlags > 0 && <span data-testid="audit-tab-badge" className="font-mono text-[10px] px-1.5 py-0.5 rounded-full bg-[#F59E0B]/15 text-[#F59E0B] border border-[#F59E0B]/40">{auditFlags}</span>}
        </button>
      </nav>

      {view === "audit" ? (
        <main className="no-print p-5 max-w-[1800px] mx-auto">
          <AuditLog entries={auditLog} loading={auditLoading} onRefresh={loadAudit} />
        </main>
      ) : (
      <main className="no-print p-5 grid grid-cols-12 gap-4 max-w-[1800px] mx-auto">
        <Zone id="inputs" {...zoneProps} className="col-span-12 lg:col-span-3">
          <InputsPanel scenario={scenario} setScenario={onChangeScenario} presets={config?.presets || []} activePreset={activePreset} onPreset={onPreset} onRecommend={() => runRecommend(scenario)} loading={loading} />
        </Zone>
        <div className="col-span-12 lg:col-span-6 space-y-4">
          <Zone id="price" {...zoneProps}>
            <HeroCard result={result} scenario={scenario} onAccept={onAccept} onOverride={onOverride} decision={decision} />
          </Zone>
          <Zone id="multipliers" {...zoneProps}>
            <MultiplierBreakdown optimization={result?.optimization} />
          </Zone>
          <Zone id="charts" {...zoneProps} className="grid grid-cols-2 gap-4">
            <ForecastChart forecast={forecast} scenario={scenario} />
            <PaceChart forecast={forecast} pace={pace} />
          </Zone>
          <Zone id="montecarlo" {...zoneProps}>
            <MonteCarloCard simulation={result?.simulation} />
          </Zone>
          <Zone id="comparison" {...zoneProps}>
            <ComparisonTable result={result} />
          </Zone>
        </div>
        <div className="col-span-12 lg:col-span-3 space-y-4 flex flex-col">
          <Zone id="warnings" {...zoneProps}>
            <WarningsBox warnings={result?.optimization.warnings} />
          </Zone>
          <Zone id="explanation" {...zoneProps} className="flex-1 flex flex-col">
            <ExplanationCard explanation={explanation} loading={explaining} onRegenerate={onRegenerate} hasResult={!!result} />
          </Zone>
        </div>
      </main>
      )}
      <PresenterMode active={presenter.active} step={presenter.step} paused={presenter.paused} secondsLeft={presenter.secondsLeft}
        spotlight={spotlight} onSpotlight={setSpotlight}
        onNext={presenterNext} onStop={stopPresenter} onTogglePause={() => setPresenter((p) => ({ ...p, paused: !p.paused }))} />
      <StrategySheet result={result} explanation={explanation} decision={decision} overridePrice={overridePrice} hotel={config?.hotel} />
    </div>
  );
}

export default App;
