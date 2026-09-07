# Plan — Project Documentation (Word File)

## Objective
Produce a single downloadable Microsoft Word document (`.docx`) that explains, in detail, how the AI Dynamic Pricing & Revenue Management Simulator works — the business logic, the maths, the AI layer, and every screen feature — so it can be submitted or circulated alongside the live classroom demo.

## Deliverable
- One file: `Hotel_Dynamic_Pricing_Simulator_Documentation.docx`
- Written for an MBA IT & Systems audience: business-first language, with the formulas and technical mechanics kept in clearly marked sections so a technical evaluator can also follow them.
- Estimated length: 18–25 pages, including captions and tables.
- Made available as a download link in the chat, and also stored inside the app so it can be re-downloaded later.

## Proposed document contents

1. **Title page** — project name, subtitle, hotel/context, date.
2. **Executive summary** — one page: what the simulator does and why dynamic pricing matters in hospitality.
3. **Problem context** — the revenue management problem: perishable inventory, fixed capacity, demand uncertainty, competitor pressure.
4. **Solution overview** — the four-zone dashboard walkthrough (scenario inputs → recommendation → analytics → guardrails and AI explanation), with annotated screenshots of the live app.
5. **How the pricing decision is made** — the full working of the optimizer:
   - The multiplier chain (base rate × season × demand × capacity/scarcity × competitor parity × lead-time × event), with what each multiplier represents and its numeric ranges.
   - The search step that tests prices around the formula price and picks the revenue-maximising one, and the occupancy constraint that stops it chasing rate at the cost of an empty hotel.
   - The price floor and ceiling rules.
   - A fully worked numeric example, tracing one scenario from sliders to final recommended rate.
6. **How customers are modelled** — the two segments (leisure = price-sensitive, business = time-sensitive), the price-response curve behind each, and how sensitivity changes as arrival approaches.
7. **The Monte Carlo simulation** — why a single revenue number is misleading, what the 500 runs do, and how to read P10 / P50 / P90, expected occupancy, conversion rate and sell-out probability.
8. **Forecasting and booking pace** — how the 14-day demand forecast and the pickup curve are produced, and how a presenter uses "ahead of / behind pace" in the narrative.
9. **Ethical and policy guardrails** — each warning rule (surge threshold, below-cost, fairness gap, competitor parity), why it exists, the flag-not-block design choice, and the audit log as the compliance answer.
10. **The AI explanation layer** — what is sent to Gemini 3 Flash, what it returns (why this price / key risks / alternative strategy), why the output is cached, the word-by-word streaming reveal, and the deterministic fallback that guarantees the demo never shows a blank panel.
11. **Presenter Mode** — the three shock scenarios, the auto-advance timing, and zone spotlight.
12. **Feature reference table** — every UI control and what it does.
13. **Assumptions and limitations** — synthetic data, single hotel and room type, no live OTA feed, no real bookings; stated plainly so the demo is not oversold.
14. **Possible extensions** — multi-property, live competitor feeds, reinforcement learning, hard policy enforcement, guest booking portal.
15. **Glossary** — ADR, RevPAR, occupancy, pace, pickup, surge, parity, P50, Monte Carlo, multiplier chain.

## Presentation choices being made
- Screenshots: real captures of the running app (dashboard, presenter mode with spotlight, audit log, strategy sheet) rather than mock-ups or drawings.
- Formulas: written as readable expressions with each term explained in a table, not as code listings. No source code is pasted into the document.
- Styling: clean professional Word formatting — headings, numbered sections, tables, figure captions, page numbers. Not styled to match the app's dark theme, since this is meant to be printed and read.
- Numbers used in worked examples come from real runs of the app so they are internally consistent.

## Assumptions
- The document is about how the product works, not a code walkthrough or API reference. If an API-level appendix is needed for a technical submission, it can be added.
- No academic report scaffolding (abstract, literature review, references, certificate page, institutional cover format) is included, since this was not requested. Say the word if the submission requires that format.
- English, INR throughout, matching the app.
- The app itself is not modified by this work — the only change is a new downloadable document.

## Open question
- If this is for a formal college submission with a prescribed report template (cover page format, abstract, literature review, references), the structure above should be reshaped to match it. Otherwise the professional-report structure above is used.
