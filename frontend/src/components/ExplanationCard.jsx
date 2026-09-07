import { Bot, RefreshCw, Lightbulb, AlertOctagon, Route } from "lucide-react";

const Block = ({ icon: Icon, title, testId, children }) => (
  <div data-testid={testId}>
    <p className="flex items-center gap-1.5 text-xs font-semibold gold-text font-heading"><Icon size={13} /> {title}</p>
    <div className="text-sm text-[#CBD5E1] leading-relaxed mt-1.5">{children}</div>
  </div>
);

export const ExplanationCard = ({ explanation, loading, onRegenerate, hasResult }) => (
  <section data-testid="llm-explanation-card" className="panel p-5 reveal flex-1">
    <div className="flex items-center justify-between">
      <div>
        <p className="eyebrow">AI explanation layer</p>
        <h3 className="font-heading text-sm font-semibold mt-0.5 flex items-center gap-1.5"><Bot size={14} className="gold-text" /> Gemini 3 Flash</h3>
      </div>
      {hasResult && (
        <button data-testid="regenerate-explanation-button" onClick={onRegenerate} disabled={loading} className="btn-ghost text-[11px] px-2.5 py-1 flex items-center gap-1">
          <RefreshCw size={11} className={loading ? "animate-spin" : ""} /> Re-generate
        </button>
      )}
    </div>
    {!hasResult ? (
      <p className="text-sm text-[#64748B] mt-4">The LLM will explain the recommendation in plain English once the optimizer runs.</p>
    ) : loading && !explanation ? (
      <div className="space-y-3 mt-4">
        {[80, 95, 70, 60].map((w, i) => <div key={i} className="h-3 rounded bg-[#181E2B] animate-pulse" style={{ width: `${w}%` }} />)}
        <p className="text-xs text-[#64748B] font-mono">thinking…</p>
      </div>
    ) : explanation ? (
      <div className="space-y-5 mt-4">
        <Block icon={Lightbulb} title="Why this price" testId="explanation-why">{explanation.why_this_price}</Block>
        <Block icon={AlertOctagon} title="Key risks" testId="explanation-risks">
          <ul className="space-y-1.5">{explanation.key_risks.map((r, i) => <li key={i} className="flex gap-2"><span className="text-[#F59E0B]">•</span><span>{r}</span></li>)}</ul>
        </Block>
        <Block icon={Route} title="Suggested alternative strategy" testId="explanation-alternative">{explanation.alternative_strategy}</Block>
        <p data-testid="explanation-source" className="font-mono text-[10px] text-[#64748B]">source: {explanation.source}{explanation.cached ? " · cached" : ""}</p>
      </div>
    ) : null}
  </section>
);
