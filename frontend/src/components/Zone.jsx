export const ZONE_LABELS = {
  inputs: "Scenario inputs",
  price: "Recommended price",
  multipliers: "Multiplier chain",
  charts: "Forecast & pace",
  montecarlo: "Monte Carlo",
  comparison: "Comparison",
  warnings: "Guardrails",
  explanation: "AI explanation",
};

export const Zone = ({ id, spotlight, onSpotlight, enabled, className = "", children }) => {
  const isOn = spotlight === id;
  const dimmed = enabled && spotlight && !isOn;
  const handleClick = (e) => {
    if (e.target.closest('button,input,a,select,textarea,[role="slider"]')) return;
    onSpotlight(isOn ? null : id);
  };
  return (
    <div
      data-testid={`zone-${id}`}
      data-spotlight={isOn ? "on" : dimmed ? "dim" : "off"}
      onClick={enabled ? handleClick : undefined}
      className={`${className} zone ${isOn ? "zone-on" : ""} ${dimmed ? "zone-dim" : ""} ${enabled ? "cursor-zoom-in" : ""}`}
    >
      {children}
    </div>
  );
};
