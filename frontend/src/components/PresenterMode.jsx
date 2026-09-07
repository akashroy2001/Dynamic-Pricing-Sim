import { useEffect, useState } from "react";
import { X, ChevronRight, Pause, Play } from "lucide-react";

export const PRESENTER_STEPS = [
  { preset: "concert", title: "Scenario 1 · Concert in Town", narrative: "Demand spikes to 175, only 35 rooms left, 5 days out. Watch the capacity and event multipliers push the rate up — and the surge guardrail light up in amber." },
  { preset: "competitor_cut", title: "Scenario 2 · Competitor −40%", narrative: "The rival drops to ₹3,000. Leisure guests are highly price-sensitive, so the optimizer trades some rate for occupancy rather than matching blindly." },
  { preset: "off_season", title: "Scenario 3 · Off-season Tuesday", narrative: "Demand index 45, 85 rooms unsold, 2 days out. The optimizer cuts price — but the cost-floor rule stops it from selling below ₹1,200 variable cost." },
];

export const PresenterMode = ({ active, step, onNext, onStop, paused, onTogglePause, secondsLeft }) => {
  const [visible, setVisible] = useState(false);
  useEffect(() => { setVisible(active); }, [active]);
  if (!visible) return null;
  const s = PRESENTER_STEPS[step];
  return (
    <div data-testid="presenter-mode-walkthrough-overlay" className="no-print fixed bottom-6 left-1/2 -translate-x-1/2 z-50 w-[720px] max-w-[92vw] panel panel-elevated p-5 shadow-2xl reveal border-[#E2B859]/50">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="eyebrow flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#E2B859] pulse-dot" /> Presenter mode · step {step + 1} of {PRESENTER_STEPS.length}</p>
          <h3 data-testid="presenter-step-title" className="font-heading text-lg font-bold mt-1">{s.title}</h3>
          <p className="text-sm text-[#CBD5E1] mt-1.5 leading-relaxed">{s.narrative}</p>
        </div>
        <button data-testid="presenter-stop-button" onClick={onStop} className="btn-ghost p-1.5"><X size={14} /></button>
      </div>
      <div className="flex items-center gap-2 mt-4">
        <button data-testid="presenter-pause-button" onClick={onTogglePause} className="btn-ghost text-xs px-3 py-1.5 flex items-center gap-1.5">{paused ? <Play size={12} /> : <Pause size={12} />} {paused ? "Resume" : "Pause"}</button>
        <button data-testid="presenter-next-button" onClick={onNext} className="btn-gold text-xs px-4 py-1.5 flex items-center gap-1.5">{step + 1 < PRESENTER_STEPS.length ? "Next scenario" : "Finish"} <ChevronRight size={13} /></button>
        <div className="ml-auto flex items-center gap-2">
          <span className="font-mono text-[11px] text-[#64748B]">{paused ? "paused" : `auto-advance in ${secondsLeft}s`}</span>
          <div className="w-28 h-1 rounded bg-[#232A3B] overflow-hidden"><div className="h-full bg-[#E2B859] transition-[width] duration-1000 ease-linear" style={{ width: `${(secondsLeft / 20) * 100}%` }} /></div>
        </div>
      </div>
    </div>
  );
};
