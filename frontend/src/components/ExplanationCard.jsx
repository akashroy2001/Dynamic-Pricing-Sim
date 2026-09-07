import { useEffect, useMemo, useState } from "react";
import { Bot, RefreshCw, Lightbulb, AlertOctagon, Route, FastForward } from "lucide-react";

const Block = ({ icon: Icon, title, testId, children }) => (
  <div data-testid={testId}>
    <p className="flex items-center gap-1.5 text-xs font-semibold gold-text font-heading"><Icon size={13} /> {title}</p>
    <div className="text-sm text-[#CBD5E1] leading-relaxed mt-1.5">{children}</div>
  </div>
);

const Cursor = () => <span className="stream-cursor" />;

export const ExplanationCard = ({ explanation, loading, onRegenerate, hasResult }) => {
  const parts = useMemo(() => {
    if (!explanation) return [];
    return [
      { id: "why", text: explanation.why_this_price || "" },
      ...(explanation.key_risks || []).map((r, i) => ({ id: `risk-${i}`, text: r || "" })),
      { id: "alt", text: explanation.alternative_strategy || "" },
    ];
  }, [explanation]);

  const { words, offsets, total } = useMemo(() => {
    const w = parts.map((p) => p.text.split(/\s+/).filter(Boolean));
    const off = [];
    let acc = 0;
    w.forEach((arr) => { off.push(acc); acc += arr.length; });
    return { words: w, offsets: off, total: acc };
  }, [parts]);

  const [shown, setShown] = useState(0);
  useEffect(() => { setShown(0); }, [explanation]);
  useEffect(() => {
    if (!total || shown >= total) return;
    const t = setTimeout(() => setShown((n) => n + 1), shown === 0 ? 240 : total > 90 ? 16 : 30);
    return () => clearTimeout(t);
  }, [shown, total]);

  const streaming = total > 0 && shown < total;
  const visible = (i) => words[i].slice(0, Math.max(0, shown - offsets[i])).join(" ");
  const started = (i) => shown > offsets[i];
  const streamingAt = (i) => streaming && started(i) && shown - offsets[i] < words[i].length;

  const riskParts = parts.map((p, i) => ({ ...p, i })).filter((p) => p.id.startsWith("risk"));
  const altIdx = parts.length - 1;

  return (
    <section data-testid="llm-explanation-card" className="panel p-5 reveal flex-1">
      <div className="flex items-center justify-between">
        <div>
          <p className="eyebrow">AI explanation layer</p>
          <h3 className="font-heading text-sm font-semibold mt-0.5 flex items-center gap-1.5"><Bot size={14} className="gold-text" /> Gemini 3 Flash</h3>
        </div>
        <div className="flex items-center gap-1.5">
          {streaming && (
            <button data-testid="explanation-skip-stream-button" onClick={() => setShown(total)} className="btn-ghost text-[11px] px-2.5 py-1 flex items-center gap-1">
              <FastForward size={11} /> Skip
            </button>
          )}
          {hasResult && (
            <button data-testid="regenerate-explanation-button" onClick={onRegenerate} disabled={loading} className="btn-ghost text-[11px] px-2.5 py-1 flex items-center gap-1">
              <RefreshCw size={11} className={loading ? "animate-spin" : ""} /> Re-generate
            </button>
          )}
        </div>
      </div>

      {!hasResult ? (
        <p className="text-sm text-[#64748B] mt-4">The LLM will explain the recommendation in plain English once the optimizer runs.</p>
      ) : loading && !explanation ? (
        <div className="space-y-3 mt-4">
          {[80, 95, 70, 60].map((w, i) => <div key={i} className="h-3 rounded bg-[#181E2B] animate-pulse" style={{ width: `${w}%` }} />)}
          <p className="text-xs text-[#64748B] font-mono">thinking…</p>
        </div>
      ) : explanation ? (
        <div className="space-y-5 mt-4" data-testid="explanation-body" data-streaming={streaming ? "true" : "false"}>
          <Block icon={Lightbulb} title="Why this price" testId="explanation-why">
            {visible(0)}{streamingAt(0) && <Cursor />}
          </Block>
          {started(1) && (
            <Block icon={AlertOctagon} title="Key risks" testId="explanation-risks">
              <ul className="space-y-1.5">
                {riskParts.filter((p) => started(p.i)).map((p) => (
                  <li key={p.id} className="flex gap-2"><span className="text-[#F59E0B]">•</span><span>{visible(p.i)}{streamingAt(p.i) && <Cursor />}</span></li>
                ))}
              </ul>
            </Block>
          )}
          {started(altIdx) && (
            <Block icon={Route} title="Suggested alternative strategy" testId="explanation-alternative">
              {visible(altIdx)}{streamingAt(altIdx) && <Cursor />}
            </Block>
          )}
          <p data-testid="explanation-source" className="font-mono text-[10px] text-[#64748B]">
            {streaming ? "streaming…" : `source: ${explanation.source}${explanation.cached ? " · cached" : ""}`}
          </p>
        </div>
      ) : null}
    </section>
  );
};
