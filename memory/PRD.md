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

## Backlog
- P1: Runs history drawer (list saved runs, reload scenario)
- P1: Streaming LLM text (typewriter) instead of single response
- P2: Presenter Mode spotlight highlighting of the zone being discussed
- P2: Warning log view for the "audit trail" Q&A talking point
- P2: USD toggle
