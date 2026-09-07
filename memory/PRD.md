# PRD — AI Dynamic Pricing & Revenue Management Simulator (Hotel)

## Original Problem Statement
Web-based classroom demo (MBA IT & Systems): revenue manager sets scenario conditions, a rule-based optimizer recommends room prices, a simulated two-segment customer market reacts (Monte Carlo), and an LLM explains the decision in plain English. Single hotel, single room type, 100 rooms, base rate ₹5000, INR, no auth, synthetic data.

## User Choices
- Currency: INR · LLM: Gemini 3 Flash (Emergent Universal Key) · Presenter Mode: yes · Frontend: JavaScript

## Architecture
- Frontend: React 19 (JS) + Tailwind + Recharts + shadcn/ui, single-screen 3-zone dark dashboard (Obsidian/Champagne Gold)
- Backend: FastAPI — `/api/config`, `/api/forecast`, `/api/pace`, `/api/optimize`, `/api/simulate`, `/api/recommend`, `/api/explain`, `/api/runs`, `/api/warnings/log`
- Engine (`backend/engine.py`, numpy only): multiplier chain → ±30% grid search maximising expected revenue s.t. occupancy ≥75%; logistic segment price-response (Leisure k≈4.5, Business k≈1.8 tightening near arrival); 500-run Monte Carlo (Poisson arrivals × binomial conversion, lognormal demand noise)
- LLM: emergentintegrations `gemini-3-flash-preview`, JSON output, cached in Mongo `explanations` by scenario hash, deterministic fallback on failure
- MongoDB collections: `explanations`, `runs`, `warning_log`

## User Personas
- Hotel revenue manager (presenter)
- Simulated Leisure (price-sensitive) and Business (time-sensitive) segments

## Core Requirements (static)
Scenario inputs + 4 shock presets · 365-day seeded forecast + 14-day chart · booking pace pickup curve · rule-based optimizer with multiplier breakdown · Monte Carlo P10/P50/P90 · amber non-blocking warnings (surge >2.5×, below cost, fairness gap, competitor parity) · LLM explanation (why / risks / alternative) · comparison table · accept/override persisted · printable strategy sheet · Presenter Mode

## Implemented (2026-06)
- All core features above; tested end-to-end (iteration_1: backend 100%, frontend 100%)
- Presets: Concert in Town (PARITY flag), Competitor −40%, Off-season Tuesday (FAIRNESS), Fully Booked Weekend (SURGE + PARITY)

## Implemented (2026-06, iteration 2 — tested, frontend 100%)
- **Streaming Explanation**: client-side typewriter reveal (~16-30ms/word) of the AI rationale, sequential why → risks → alternative, blinking gold caret, `Skip` button, `streaming…` source label (`ExplanationCard.jsx`)
- **Zone Spotlight**: `Zone.jsx` wrapper (`data-testid=zone-*`, `data-spotlight=on|dim|off`); presenter steps auto-spotlight (price → comparison → guardrails), manual override via chips in the presenter overlay or clicking any panel; spotlighted zone scrolls into view; interactive elements never hijack clicks
- **Warning Audit Log**: new dashboard tab (`tab-audit-log`) reading `GET /api/warnings/log` — timestamped flags with price + scenario chips, flag/event totals, refresh, amber badge on the tab. Screen-only (excluded from printable strategy sheet) per user choice

## Backlog
- P1: Runs history drawer (list saved runs, reload scenario)
- P2: USD toggle
- P2: Multi-room-type & multi-property support
- P2: Real competitor pricing via OTA APIs
- P2: Reinforcement-learning pricing agent
- P2: Hard policy enforcement (block, not just flag) with sign-off trail
- P2: Guest booking portal to close the loop
