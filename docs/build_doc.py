"""Builds the project documentation .docx for the Hotel Dynamic Pricing Simulator."""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "docs")
OUT = os.path.join(OUT_DIR, "Hotel_Dynamic_Pricing_Simulator_Documentation.docx")
ACCENT = RGBColor(0x8A, 0x62, 0x00)

doc = Document()

# ---------- base styles ----------
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(8)
normal.paragraph_format.line_spacing = 1.15
for name, size in (("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 12)):
    st = doc.styles[name]
    st.font.name = "Calibri Light"
    st.font.size = Pt(size)
    st.font.color.rgb = RGBColor(0x1F, 0x28, 0x37)
    st.font.bold = True

for s in doc.sections:
    s.left_margin = s.right_margin = Inches(1.0)
    s.top_margin = s.bottom_margin = Inches(0.9)

fig_counter = {"n": 0}
tbl_counter = {"n": 0}


def field(par, instr):
    r = par.add_run()
    f1, it, f2 = OxmlElement("w:fldChar"), OxmlElement("w:instrText"), OxmlElement("w:fldChar")
    f1.set(qn("w:fldCharType"), "begin")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    f2.set(qn("w:fldCharType"), "end")
    r._r.append(f1); r._r.append(it); r._r.append(f2)


def footer_page_numbers():
    p = doc.sections[0].footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("The Grand Horizon Palace · AI Dynamic Pricing & Revenue Management Simulator · Page ").font.size = Pt(8)
    field(p, "PAGE")
    p.add_run(" of ").font.size = Pt(8)
    field(p, "NUMPAGES")
    for r in p.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(0x60, 0x60, 0x60)


def h1(text):
    doc.add_heading(text, 1)


def h2(text):
    doc.add_heading(text, 2)


def h3(text):
    doc.add_heading(text, 3)


def p(text, italic=False, bold=False, size=11):
    par = doc.add_paragraph()
    r = par.add_run(text)
    r.italic = italic
    r.bold = bold
    r.font.size = Pt(size)
    return par


def bullets(items, style="List Bullet"):
    for it in items:
        par = doc.add_paragraph(style=style)
        if isinstance(it, tuple):
            par.add_run(it[0] + " ").bold = True
            par.add_run(it[1])
        else:
            par.add_run(it)


def formula(text):
    par = doc.add_paragraph()
    par.paragraph_format.left_indent = Inches(0.3)
    par.paragraph_format.space_before = Pt(6)
    r = par.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(10.5)
    r.font.color.rgb = ACCENT
    r.bold = True


def figure(filename, caption, width=6.2):
    path = os.path.join(IMG, filename)
    if not os.path.exists(path):
        return
    fig_counter["n"] += 1
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(path, width=Inches(width))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run(f"Figure {fig_counter['n']}: {caption}")
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x50, 0x50, 0x50)


def table(headers, rows, caption=None, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    for i, hd in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(hd)
        run.bold = True
        run.font.size = Pt(9.5)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(val))
            run.font.size = Pt(9.5)
    if widths:
        for r_ in t.rows:
            for i, w in enumerate(widths):
                r_.cells[i].width = Inches(w)
    if caption:
        tbl_counter["n"] += 1
        cap = doc.add_paragraph()
        r = cap.add_run(f"Table {tbl_counter['n']}: {caption}")
        r.italic = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x50, 0x50, 0x50)
    doc.add_paragraph()


def pagebreak():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


footer_page_numbers()

# ============================ 1. TITLE PAGE ============================
for _ in range(4):
    doc.add_paragraph()
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("AI Dynamic Pricing &\nRevenue Management Simulator")
r.bold = True
r.font.size = Pt(30)
r.font.name = "Calibri Light"

st = doc.add_paragraph()
st.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = st.add_run("How the system works — business logic, pricing mathematics,\ncustomer simulation and the AI explanation layer")
r.font.size = Pt(13)
r.italic = True
r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

doc.add_paragraph()
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("Case setting: The Grand Horizon Palace, Mumbai — 100 rooms, single room type\nBase rate ₹5,000 · Currency: Indian Rupee (INR)")
r.font.size = Pt(11)

for _ in range(6):
    doc.add_paragraph()
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = meta.add_run("Prepared for an MBA (IT & Systems) classroom demonstration\nJune 2026")
r.font.size = Pt(11)
r.bold = True
pagebreak()

# ============================ CONTENTS ============================
h1("Contents")
p("This document is organised in fifteen numbered sections. If the table of contents below appears empty, "
  "right-click it in Microsoft Word and choose \u201cUpdate Field\u201d to populate it.", italic=True, size=10)
toc = doc.add_paragraph()
field(toc, 'TOC \\o "1-2" \\h \\z \\u')
pagebreak()

# ============================ 2. EXECUTIVE SUMMARY ============================
h1("1. Executive summary")
p("The AI Dynamic Pricing & Revenue Management Simulator is a working web application that lets a hotel revenue "
  "manager set the conditions of a single night — how strong demand is, how many rooms are still unsold, how far away "
  "the arrival date is, what the competitor is charging, whether an event is in town — and instantly see the room rate "
  "that maximises expected revenue, the revenue range that rate is likely to produce, the ethical flags it raises, and "
  "a plain-English explanation of the decision written by an AI model.")
p("It is built for teaching. Every number on screen is produced by a transparent rule, and the rule is shown next to "
  "the number, so a class can argue with the recommendation rather than simply accept it. The simulator answers four "
  "questions that sit at the heart of hospitality revenue management:")
bullets([
    ("What should we charge tonight?", "a rule-based optimizer converts scenario conditions into a recommended rate."),
    ("How confident are we?", "a 500-run Monte Carlo simulation of guest behaviour turns a single revenue figure into a P10–P50–P90 range."),
    ("Is the price defensible?", "four policy guardrails flag surge, below-cost, fairness and parity problems without blocking the manager."),
    ("Can we explain it to a human?", "Google's Gemini 3 Flash converts the mathematics into a short business rationale, with risks and an alternative strategy."),
])
p("The application is a browser-based dashboard (React) backed by a Python service (FastAPI) that holds the pricing "
  "engine, the customer-demand simulation and the AI integration, with MongoDB storing saved decisions, cached "
  "explanations and the compliance audit trail. All data is synthetic and generated deterministically, so a live "
  "demonstration produces the same numbers every time it is run.")

figure("doc_dashboard_top.jpeg", "The complete decision screen. Zone 1 (left) holds the scenario inputs and shock presets, Zone 2 (centre) the recommendation and analytics, Zone 3 (right) the policy guardrails and the AI explanation.")
pagebreak()

# ============================ 3. PROBLEM CONTEXT ============================
h1("2. The problem: why hotel pricing is hard")
p("A hotel room is the textbook example of perishable inventory. Tonight's unsold room cannot be stored and sold "
  "tomorrow; at midnight its value becomes zero. At the same time capacity is fixed in the short run — a hotel cannot "
  "add a floor because a concert came to town, and it cannot remove one because it is monsoon Tuesday. Between those "
  "two facts sits the entire discipline of revenue management: selling a fixed, perishable inventory to the right guest "
  "at the right time for the right price.")

h2("2.1 The four pressures on the price")
bullets([
    ("Demand uncertainty.", "The manager never knows tomorrow's demand, only a forecast with a band around it. Pricing "
     "for the average case leaves money on the table in good weeks and empties the hotel in bad ones."),
    ("Time pressure.", "Willingness to pay changes as the arrival date approaches. Leisure guests book early and shop "
     "on price; business guests book late and shop on availability. The same room is therefore worth different amounts "
     "to different guests on different days."),
    ("Competitor pressure.", "Rates are public. A rival across the road can cut 40% overnight and instantly reshape the "
     "conversion curve for every price-sensitive guest looking at the same online travel agency page."),
    ("Cost and reputation floors.", "Every occupied room costs money to service, so there is a price below which "
     "selling destroys value. Equally, there is a price above which selling damages the brand — charging five times the "
     "normal rate during a crisis is legal in most places and indefensible in all of them."),
])

h2("2.2 What the manager is actually optimising")
p("The instinct to \u201cfill the hotel\u201d and the instinct to \u201cprotect the rate\u201d pull in opposite directions. "
  "The quantity that matters is neither occupancy nor average daily rate on its own, but revenue per available room:")
formula("RevPAR  =  Occupancy  ×  ADR        Expected revenue  =  Price  ×  Expected bookings at that price")
p("Because bookings fall as price rises, expected revenue is a curve with a peak, not a line. The purpose of this "
  "simulator is to make that curve visible, to show where the peak sits under a given set of conditions, and to show "
  "how far the peak moves when a single condition — demand, scarcity, lead time, competitor rate — changes.")

# ============================ 4. SOLUTION OVERVIEW ============================
pagebreak()
h1("3. Solution overview: the four zones")
p("The application is a single screen, deliberately, so that a presenter never navigates away from the decision. It is "
  "divided into three visible zones plus a fourth compliance view reached from the tab bar.")

table(
    ["Zone", "Purpose", "What the presenter does here"],
    [
        ["Zone 1 — Manager panel", "Scenario inputs: five sliders, a season selector, an event switch and four one-click shock presets.", "Sets up the night being priced, or fires a preset to change the world instantly."],
        ["Zone 2 — Recommendation & analytics", "Recommended rate, multiplier chain, 14-day forecast, booking pace curve, Monte Carlo distribution, comparison table.", "Reads out the price, then justifies it with the forecast, the pace and the revenue distribution."],
        ["Zone 3 — Guardrails & AI", "Ethical and policy warnings, plus the Gemini 3 Flash rationale that streams in word by word.", "Shows that the model can be challenged, and lets the AI defend the number in business language."],
        ["Zone 4 — Warning audit log", "A timestamped server-side record of every guardrail flag ever raised.", "Answers the compliance question: \u201ccan you prove what the system flagged, and when?\u201d"],
    ],
    caption="The four zones of the simulator and their role in a live demonstration.",
    widths=[1.5, 2.6, 2.1],
)

h2("3.1 The flow of a single decision")
p("One decision moves through the system in a fixed sequence, and the whole sequence completes in well under a second "
  "for the pricing mathematics, with the AI explanation arriving a moment later:")
bullets([
    "The manager sets the scenario, or clicks a shock preset which sets all seven inputs at once.",
    "The optimizer builds the multiplier chain, produces a formula price, then searches prices around it and selects the revenue-maximising rate that still respects the occupancy constraint and the price bounds.",
    "The customer simulation runs 500 times at the recommended rate, and again at the current rate and the competitor rate, so the three options can be compared on the same basis.",
    "The guardrail rules are evaluated against the recommended rate; any flag raised is written to the audit log with a timestamp.",
    "The scenario, the recommendation and the simulation summary are sent to Gemini 3 Flash, which returns a rationale, three key risks and an alternative strategy.",
    "The manager accepts the price or overrides it; either way the decision is stored, and the strategy sheet can be printed.",
], style="List Number")

figure("doc_inputs.png", "Zone 1, the manager panel: five sliders, the season selector, the event switch and the four shock presets.", width=3.4)

# ============================ 5. OPTIMIZER ============================
pagebreak()
h1("4. How the pricing decision is made")
p("The recommendation is produced in three steps: a transparent multiplier chain gives a starting price, a bounded "
  "search around that price finds the revenue-maximising rate, and two hard rules keep the answer inside a defensible "
  "range. Nothing here is a black box — this is deliberate, because the class needs to be able to disagree with each "
  "individual multiplier.")

h2("4.1 Step one: the multiplier chain")
p("The starting point, called the formula price on screen, is the base rate adjusted by seven independent factors, "
  "each answering one business question:")
formula("Formula price = BaseRate × Season × Demand × CapacityScarcity × CompetitorAdj × LeadTime × Event")

table(
    ["Multiplier", "Business question it answers", "How it is calculated", "Range"],
    [
        ["Base rate", "What is this room normally worth?", "Fixed property parameter", "₹5,000"],
        ["Season", "Is this a high or low season?", "Peak 1.25 · Shoulder 1.00 · Off-season 0.80", "0.80 – 1.25"],
        ["Demand", "Is the market hotter or colder than normal?", "1 + 0.4 × (DemandIndex ÷ 100 − 1), then clipped", "0.65 – 1.40"],
        ["Capacity scarcity", "How little is left to sell?", "1 + 0.5 × (1 − RemainingShare)²", "1.00 – 1.50"],
        ["Competitor adjustment", "Where is the market rate?", "1 + 0.3 × (CompetitorPrice ÷ BaseRate − 1), then clipped", "0.75 – 1.25"],
        ["Lead time", "How close is arrival?", "≤3 days 1.15 · ≤7 days 1.08 · ≤21 days 1.00 · beyond 0.93", "0.93 – 1.15"],
        ["Event", "Is there a demand shock in the city?", "1.20 when the event switch is on, otherwise 1.00", "1.00 – 1.20"],
    ],
    caption="The seven multipliers, their business meaning and their permitted ranges.",
    widths=[1.3, 1.9, 2.2, 0.8],
)

p("Three design choices in this table are worth defending explicitly in class:")
bullets([
    ("Demand is damped.", "A demand index 75% above normal does not justify a rate 75% above normal, because guests "
     "shop across hotels. Only 40% of the demand movement is passed into price, and the result is capped at 1.40."),
    ("Scarcity is convex, not linear.", "Because the term is squared, the first rooms sold barely move the rate while "
     "the last few move it sharply — which mirrors how a real revenue manager behaves as a date closes out."),
    ("The competitor is a reference, not a rule.", "Only 30% of the competitor's deviation from the base rate is "
     "absorbed, and the effect is clipped at ±25%, so the hotel never blindly follows a rival into a price war."),
])
figure("doc_multipliers.png", "The multiplier chain shown on screen for the concert scenario, ending at the formula price and then the revenue-maximising rate.", width=6.2)

h2("4.2 Step two: the revenue-maximising search")
p("The formula price is a sensible starting point, not the answer. The optimizer therefore builds a grid of candidate "
  "prices from 30% below to 30% above the formula price in ₹50 steps, and for every candidate it estimates how many "
  "rooms each guest segment would book at that price and what revenue would result. The candidate with the highest "
  "expected revenue wins.")
formula("Recommended price = argmax over candidate prices of  ( Price × Expected bookings at that price )")
p("This is the single most important idea in the tool: the recommendation is not the highest price the rules allow, it "
  "is the price at which the trade-off between rate and volume produces the most money. Raising the rate further is "
  "rejected by the optimizer itself, not by a policy.")

h3("The occupancy constraint")
p("A pure revenue maximiser can be happy with a half-empty hotel at a very high rate. Real properties are not, because "
  "empty rooms damage food-and-beverage revenue, staff morale and online ranking. The optimizer therefore only "
  "considers candidates that are expected to fill at least 75% of the rooms still unsold. If no candidate can clear "
  "that bar — a genuinely dead night — the constraint is relaxed rather than returning nothing, and the screen "
  "indicates that the constraint was binding.")

h3("Floor and ceiling")
p("Two absolute bounds sit outside the search. The price can never fall below 0.2× the base rate (₹1,000) or rise above "
  "3.0× the base rate (₹15,000). Separately, the variable cost of servicing an occupied room is ₹1,200, and any "
  "recommendation below that cost raises a below-cost warning, because selling under cost converts an empty room into "
  "a loss-making one.")

# ---- worked example ----
pagebreak()
h2("4.3 A fully worked example: \u201cConcert in Town\u201d")
p("The following trace uses the concert shock preset exactly as the application computes it, so every figure below can "
  "be reproduced live on screen.")
table(
    ["Scenario input", "Value", "Reading"],
    [
        ["Base demand index", "175", "Market running 75% hotter than a normal night"],
        ["Capacity remaining", "35% (35 of 100 rooms)", "Two thirds of the hotel is already sold"],
        ["Days to arrival", "5", "Inside the business-traveller booking window"],
        ["Season", "Shoulder", "No seasonal uplift"],
        ["Competitor average price", "₹8,200", "The market has already repriced upward"],
        ["Event in town", "Yes", "Stadium show, roughly 40,000 visitors"],
        ["Current price", "₹5,000", "The rate the hotel is live with today"],
    ],
    caption="Scenario inputs for the worked example.",
    widths=[2.0, 1.7, 2.5],
)

p("Multiplier chain:", bold=True)
formula("₹5,000 × 1.00 (season) × 1.30 (demand) × 1.211 (scarcity) × 1.192 (competitor) × 1.08 (lead time) × 1.20 (event) = ₹12,160")
p("Each term traced back to its input: demand 1 + 0.4 × (1.75 − 1) = 1.30; scarcity 1 + 0.5 × (1 − 0.35)² = 1.211; "
  "competitor 1 + 0.3 × (8,200 ÷ 5,000 − 1) = 1.192; lead time 1.08 because arrival is five days out; event 1.20.")

p("Search step:", bold=True)
p("The optimizer tests every rate from ₹8,512 to ₹15,000 in ₹50 steps. Expected revenue peaks at ₹12,412 — slightly "
  "above the formula price, because with only 35 rooms left and event-driven demand the hotel is expected to sell out "
  "even at that rate. At ₹12,412 the model expects all 35 remaining rooms to go, producing roughly ₹4.34 lakh of "
  "revenue for the night against ₹1.75 lakh at the current ₹5,000 rate.")

table(
    ["Quantity", "At current ₹5,000", "At recommended ₹12,412", "At competitor ₹8,200"],
    [
        ["Leisure conversion", "93.3%", "31.4%", "70.6%"],
        ["Business conversion", "87.9%", "52.4%", "73.1%"],
        ["Expected bookings (capped at 35 rooms)", "35.0", "35.0", "35.0"],
        ["Expected revenue", "₹1,75,000", "₹4,34,420", "₹2,87,000"],
        ["Monte Carlo P50 revenue", "₹1,75,000", "₹4,34,420", "₹2,87,000"],
    ],
    caption="Why the higher rate wins: conversion falls sharply, but demand is deep enough that the last 35 rooms still sell.",
    widths=[2.2, 1.4, 1.5, 1.3],
)
p("The teaching point is the third row. Conversion collapses from 93% to 31% for leisure guests, and the recommendation "
  "is still correct — because the hotel only needs 35 bookings, and even a 31% conversion on event-inflated demand "
  "delivers them. Change the scenario so that 85 rooms are unsold and the same logic produces a far lower rate.")
figure("doc_hero.png", "The recommendation card for the worked example: the rate, the uplift against the current price, the revenue range and the expected occupancy.", width=6.2)

# ============================ 6. CUSTOMER MODEL ============================
pagebreak()
h1("5. How customers are modelled")
p("Every expected-revenue figure in the tool rests on an assumption about how guests react to price. Two segments are "
  "modelled, because a single \u201caverage guest\u201d hides the most interesting behaviour in hotel pricing.")

table(
    ["Segment", "Share of demand", "Baseline conversion", "Price sensitivity (k)", "Behaviour"],
    [
        ["Leisure", "60%", "55%", "≈ 4.5", "Books early, compares hotels, walks away when the rate rises above the market reference"],
        ["Business", "40%", "65%", "≈ 1.8", "Books late, needs a room on a specific date, far less responsive to price"],
    ],
    caption="The two simulated demand segments.",
    widths=[1.0, 1.1, 1.2, 1.3, 2.2],
)

h2("5.1 The price-response curve")
p("Each segment converts according to a logistic curve centred on a market reference price. Below the reference the "
  "segment converts at close to its natural ceiling; above it conversion decays, and the speed of that decay is the "
  "segment's sensitivity:")
formula("Conversion(P) = 2 × BaselineConversion ÷ ( 1 + exp( k × ( P ÷ ReferencePrice − 1 ) ) )   , bounded to 2%–95%")
p("A high k produces a cliff: a 20% premium over the reference destroys most of the segment's bookings. A low k "
  "produces a slope: the same premium costs relatively few bookings. This one parameter is what makes business demand "
  "profitable to price into and leisure demand dangerous to price into.")

h3("The reference price")
p("The reference is the price the market has taught guests to expect for this night. It blends the competitor rate with "
  "the hotel's own base rate and then adjusts for the conditions of the night:")
formula("Reference = (0.5 × Competitor + 0.5 × BaseRate) × 1.15 × SeasonDemand × Event(1.15) × Scarcity × Urgency")
p("For the worked example this gives roughly ₹9,835, which is why a ₹12,412 rate — a 26% premium over the reference — "
  "still converts a third of leisure demand rather than none of it.")

h2("5.2 Sensitivity changes as arrival approaches")
p("The two segments move in opposite directions as the date closes in, and this is modelled explicitly:")
bullets([
    ("Business demand hardens.", "Sensitivity falls from 1.8 to 1.5 inside a week and to 1.2 inside three days. A guest "
     "who must be in Mumbai on Thursday will pay for Thursday."),
    ("Leisure demand softens or hardens with context.", "Sensitivity rises by 1.0 in the off-season, when guests are "
     "purely bargain-hunting, and falls by 1.0 when an event is in town, because attending the event is the reason for "
     "the trip and the room is a means to it."),
])

h2("5.3 How much demand exists in the first place")
p("Conversion only matters if there is traffic to convert. Potential demand for the night is derived from the rooms "
  "still available, scaled by the market conditions:")
formula("Potential demand = max(RoomsRemaining, 8) × DemandIndex ÷ 100 × SeasonDemand × Event(1.25) × LeadTime(1.15 within a week)")
p("In the worked example this is 35 × 1.75 × 1.00 × 1.25 × 1.15 ≈ 88 potential guests chasing 35 rooms — which is "
  "precisely the condition under which a rate rise is the correct commercial answer.")

# ============================ 7. MONTE CARLO ============================
pagebreak()
h1("6. The Monte Carlo simulation")
p("The optimizer produces one revenue number. Presenting that number alone would be the single most misleading thing "
  "the tool could do, because it implies a certainty that does not exist. The simulator therefore runs the night 500 "
  "times with random variation and reports the distribution of outcomes.")

h2("6.1 What varies across the 500 runs")
bullets([
    ("Demand volume.", "Arrivals are drawn from a Poisson distribution whose mean is itself multiplied by log-normal "
     "noise, so some nights simply attract more enquiries than others."),
    ("Conversion behaviour.", "The modelled conversion rate is perturbed by roughly ±12% each run, representing guests "
     "who behave better or worse than the curve predicts."),
    ("Booking outcome.", "Each arriving guest either books or does not, drawn as a binomial outcome — so even identical "
     "traffic and identical conversion produce different room counts."),
    ("Physical capacity.", "Bookings are capped at rooms actually available, which is what creates the flat ceiling "
     "visible at the right-hand side of the revenue histogram on a sell-out night."),
])

h2("6.2 How to read the output")
table(
    ["Metric", "Meaning", "Worked example"],
    [
        ["P10 revenue", "The pessimistic case — nine runs in ten did better than this", "₹3,10,300"],
        ["P50 revenue", "The median outcome, the honest headline number", "₹4,34,420"],
        ["P90 revenue", "The optimistic case — only one run in ten did better", "₹4,34,420 (capped by sell-out)"],
        ["Expected occupancy", "Average share of the whole hotel occupied by morning", "96.8%"],
        ["Conversion rate", "Share of potential guests who actually booked", "36.1%"],
        ["Sell-out probability", "Share of runs in which every remaining room sold", "51%"],
    ],
    caption="Reading the Monte Carlo panel for the worked example.",
    widths=[1.5, 3.4, 1.3],
)
p("Two of these rows carry the argument. First, P10 and P90 collapsing to the same value is not a bug — it is the "
  "signature of a capacity-constrained night, where the hotel cannot do better than selling out and the only remaining "
  "risk is on the downside. Second, a 51% sell-out probability is the honest answer to \u201cwill this work?\u201d: it is a "
  "coin toss on a full house, with a well-defined revenue floor if it misses.")
figure("doc_montecarlo.png", "The revenue distribution across 500 simulated runs, with P10, P50 and P90 markers and the segment split.", width=6.2)

h2("6.3 The comparison view")
p("The same simulation is run at three prices — the hotel's current rate, the recommended rate and the competitor's "
  "rate — so that the three strategies are compared on identical assumptions rather than on intuition. This is the "
  "panel that answers the most common objection in the room, which is \u201cwe should just match the competitor\u201d.")
figure("doc_comparison.png", "Current versus recommended versus matching the competitor, on identical simulated demand.", width=6.2)

# ============================ 8. FORECAST & PACE ============================
pagebreak()
h1("7. Forecasting and booking pace")
h2("7.1 The 14-day demand forecast")
p("The tool generates 365 days of synthetic demand history from a fixed random seed, then projects the next fourteen "
  "days. Demand is built from three components, which is exactly how a real forecast is decomposed:")
formula("Demand = Seasonal wave (annual + half-year harmonic) × Day-of-week effect + Random noise")
bullets([
    ("Seasonality.", "An annual sine wave with a secondary half-year harmonic, so the year has a main high season and a "
     "secondary shoulder peak rather than one smooth hump."),
    ("Day of week.", "Friday 1.15, Saturday 1.18, Sunday 0.90, and midweek Tuesday and Wednesday 0.94 — the classic "
     "leisure-property weekly shape."),
    ("Noise.", "Normally distributed daily variation, so no two comparable dates are identical."),
])
p("The forward view widens as it extends: the confidence band around day one is narrow and grows by roughly 1.2 index "
  "points per day out. This visual widening is the point — it shows the class that a forecast is a cone, not a line, "
  "and that pricing decisions fourteen days out deserve less conviction than decisions tomorrow.")

h2("7.2 The booking pace curve")
p("Pace answers a different question from the forecast: not \u201chow much demand is there?\u201d but \u201care we selling it fast "
  "enough?\u201d. The expected share of rooms sold by a given number of days before arrival follows an exponential pickup "
  "curve:")
formula("Expected share sold = 100 × e^(−DaysToArrival ÷ 12)        Pace index = Actual sold ÷ Expected sold")
p("The curve is deliberately steep near arrival, because most bookings in a city hotel arrive in the final fortnight. "
  "The pace index turns it into a single verdict the presenter can use as a sentence:")
bullets([
    ("Pace index above 1.1", "— ahead of pace, the hotel is selling faster than the curve, hold or push the rate."),
    ("Pace index near 1.0", "— on the books as expected, the rate is roughly right."),
    ("Pace index below 0.9", "— behind pace, demand is not converting, the rate needs to come down or promotion needs to go up."),
])
p("In the worked example 65% of the hotel is sold with five days to go against an expected 65.9%, giving a pace index "
  "of 0.99 — precisely on pace, which is why the recommendation is driven by scarcity and the event rather than by a "
  "pace correction.")
figure("doc_charts.png", "The 14-day demand forecast with its widening confidence band (left) and the booking pace curve with the current position marked (right).", width=6.4)

# ============================ 9. GUARDRAILS ============================
pagebreak()
h1("8. Ethical and policy guardrails")
p("A pricing engine that only maximises revenue will eventually recommend something a hotel cannot defend in public. "
  "The simulator evaluates four rules against every recommendation and raises an amber flag when one is breached, with "
  "a specific mitigation attached.")

table(
    ["Flag", "Trigger", "Why the rule exists", "Suggested mitigation"],
    [
        ["SURGE", "Recommended rate above 2.5× the base rate", "Extreme surge pricing during events or emergencies creates reputational and regulatory exposure", "Cap at 2.5×, or add value (breakfast, late checkout) to justify the premium"],
        ["BELOW COST", "Recommended rate below the ₹1,200 variable cost per occupied room", "Selling below the cost of servicing a room converts an empty room into a loss", "Hold at the cost floor and accept lower occupancy"],
        ["FAIRNESS", "Segment-optimal rates differ by more than 50%", "Charging one type of guest far more than another for the same room invites discrimination claims", "Use fenced rates (advance purchase, non-refundable) rather than segment-based pricing"],
        ["PARITY", "Recommended rate more than 40% above the competitor", "Leisure conversion collapses and online travel agency ranking suffers", "Monitor pickup daily and be ready to step down in ₹250 increments"],
    ],
    caption="The four guardrail rules.",
    widths=[0.9, 1.6, 2.1, 1.8],
)

h2("8.1 Flag, do not block")
p("This is a deliberate design decision, and it is the most discussion-worthy choice in the product. The system never "
  "refuses to show a price. It shows the price, shows the flag, and leaves the decision with the human. Two arguments "
  "support this:")
bullets([
    "A hard block hides the trade-off. If the tool silently caps the rate at 2.5×, the manager never learns what the "
    "unconstrained optimum was, and cannot make an informed judgement about whether the flag is worth accepting.",
    "Accountability requires a decision-maker. A blocked recommendation makes the algorithm responsible for the "
    "outcome; a flagged recommendation keeps a named human responsible, which is where regulators and boards expect it "
    "to sit.",
])
p("The counter-argument, which a class should be invited to make, is that flags become wallpaper. A manager who sees "
  "an amber box on every high-demand night stops reading it. That is exactly why the audit log exists.")
figure("doc_warnings.png", "A parity flag raised on the worked example, with the reason and the mitigation attached.", width=5.2)

h2("8.2 The audit log as the compliance answer")
p("Every flag is written to the database at the moment it is raised, together with the rate, the full scenario that "
  "produced it and a timestamp. The Warning audit log tab replays that history newest-first, with running totals of "
  "events and flags, so the question \u201cwhat did the system warn you about, and when?\u201d has a documented answer rather "
  "than a recollection. The log is a screen-only compliance view: it is intentionally excluded from the printable "
  "strategy sheet, which stays a one-page decision document.")
figure("doc_audit.jpeg", "The warning audit log: each entry carries a timestamp, the recommended rate, the scenario conditions and every flag raised.", width=6.4)

# ============================ 10. AI LAYER ============================
pagebreak()
h1("9. The AI explanation layer")
p("The mathematics produces a defensible number. It does not produce a defensible sentence, and in a hotel the price "
  "has to be explained to a general manager, an owner and sometimes a guest. The AI layer exists to close that gap.")

h2("9.1 What is sent to the model")
p("Each explanation request sends a compact, purely numerical brief — no free text, no source code, and nothing "
  "about individual guests:")
bullets([
    "Property parameters: room count, base rate and variable cost.",
    "The full scenario: demand index, capacity remaining, days to arrival, season, competitor rate, event flag and current price.",
    "The recommendation: the formula price, the final recommended rate and every multiplier in the chain.",
    "The expected outcome at the recommended rate and at the current rate.",
    "The Monte Carlo summary: P10, P50 and P90 revenue, expected occupancy, conversion rate and sell-out probability.",
    "The titles of any guardrail flags raised.",
])

h2("9.2 What comes back")
p("The model used is Google Gemini 3 Flash, chosen for response speed because the tool is used live in front of an "
  "audience. It is instructed to answer as a senior revenue manager speaking to MBA students, to cite the numbers it "
  "was given, to avoid jargon, and to return exactly three things:")
bullets([
    ("Why this price", "— two or three sentences connecting the conditions to the rate."),
    ("Key risks", "— three short, specific risks, not generic caveats."),
    ("Alternative strategy", "— a different defensible course of action, so the recommendation reads as a choice rather than a verdict."),
])
p("For the worked example the model explains that with only 35 rooms left and an event driving a demand index of 175, "
  "the rate is being raised aggressively to capture roughly ₹4.34 lakh against ₹1.75 lakh at the base rate, by "
  "targeting price-insensitive business travellers booking late; it flags the 51% premium over the competitor, the "
  "coin-toss sell-out probability and the loss of leisure guests as risks; and it offers ₹9,500 as the more "
  "conservative alternative that would secure a faster sell-out.")
figure("doc_explanation.png", "The AI explanation panel: rationale, three risks, an alternative strategy, and the source line showing which model answered.", width=4.6)

h2("9.3 Three engineering decisions that matter in a live demo")
bullets([
    ("Caching.", "Each explanation is stored against a hash of the scenario and the rounded price. Re-running the same "
     "scenario returns the stored text instantly and marks it as cached, so repeating a scenario on stage costs no "
     "waiting and no additional model usage. A Re-generate button forces a fresh answer when the presenter wants one."),
    ("Streaming reveal.", "The rationale is revealed word by word with a blinking caret, so the audience reads at the "
     "pace of the narration instead of being handed a wall of text. A Skip control completes the text instantly if "
     "time is short."),
    ("Deterministic fallback.", "If the model is unreachable or returns something unusable, the application composes an "
     "explanation itself from the three strongest multipliers, the revenue delta and the simulated revenue spread, and "
     "labels the source as fallback. The panel is therefore never blank, and the demonstration cannot be derailed by "
     "the network."),
])

# ============================ 11. PRESENTER MODE ============================
pagebreak()
h1("10. Presenter Mode")
p("Presenter Mode turns the dashboard into a guided narrative. It walks through three shock scenarios, each on a "
  "20-second auto-advance with pause and manual advance available, and each accompanied by a scripted narration line so "
  "the presenter never has to remember what to point at.")

table(
    ["Step", "Scenario", "Conditions", "The teaching point"],
    [
        ["1", "Concert in Town", "Demand 175, 35 rooms left, 5 days out, competitor ₹8,200, event on", "Scarcity and event multipliers push the rate up, and the parity guardrail lights up amber"],
        ["2", "Competitor −40%", "Demand 95, 60 rooms left, 10 days out, competitor ₹3,000", "The optimizer trades rate for occupancy rather than matching a rival blindly"],
        ["3", "Off-season Tuesday", "Demand 45, 85 rooms left, 2 days out, off-season", "The rate is cut, but the cost floor prevents selling below the ₹1,200 servicing cost"],
    ],
    caption="The three-step presenter walkthrough. A fourth preset, Fully Booked Weekend, is available manually and triggers both the surge and parity flags.",
    widths=[0.4, 1.4, 2.2, 2.4],
)

h2("10.1 Zone spotlight")
p("During the walkthrough the dashboard dims every panel except the one being discussed, which is highlighted and "
  "scrolled into view. Each step spotlights its own panel automatically — the recommendation for step one, the "
  "comparison table for step two, the guardrails for step three — and the presenter can override this at any moment, "
  "either by clicking a panel directly or by using the zone chips in the presenter overlay. Sliders, buttons and other "
  "controls remain fully usable while a spotlight is active, so the presenter can still change an input mid-narration.")
figure("doc_presenter_price.jpeg", "Presenter Mode, step one: the recommendation is spotlighted and the rest of the dashboard is dimmed. The overlay carries the narration, the timer and the zone chips.", width=6.4)
figure("doc_presenter_warnings.jpeg", "The same walkthrough with the spotlight moved manually to the guardrails panel.", width=6.4)

h2("10.2 The printable strategy sheet")
p("At any point the presenter can print a one-page strategy sheet: the scenario, the recommended rate and the decision "
  "taken, the exact rules and multiplier arithmetic used, every policy warning raised, and the AI rationale. It prints "
  "on white with the interface chrome removed, so it can be handed round as the artefact of the decision. The audit log "
  "is deliberately not part of this sheet.")
figure("doc_strategy_sheet.jpeg", "The printable strategy sheet for the worked example.", width=6.0)

# ============================ 12. FEATURE REFERENCE ============================
pagebreak()
h1("11. Feature reference")
p("Every control on the screen and what it does.")
table(
    ["Control", "Location", "Effect"],
    [
        ["Base demand index (0–200)", "Zone 1", "Sets how hot the market is; 100 is a normal night. Drives the demand multiplier and potential demand."],
        ["Capacity remaining (0–100%)", "Zone 1", "Rooms still unsold. Drives the scarcity multiplier, the pace comparison and the booking cap."],
        ["Days to arrival (1–90)", "Zone 1", "Sets the lead-time multiplier, tightens business price sensitivity and positions the pace marker."],
        ["Competitor average price", "Zone 1", "Moves the competitor adjustment and the market reference price, and is the basis of the parity flag."],
        ["Your current price", "Zone 1", "The live rate; used as the comparison baseline and the uplift percentage."],
        ["Season selector", "Zone 1", "Peak, shoulder or off-season; changes both the price multiplier and the underlying demand level."],
        ["Event in town switch", "Zone 1", "Adds 20% to price and 25% to demand, and makes leisure guests less price-sensitive."],
        ["Recommend Price", "Zone 1", "Runs the optimizer, the three simulations and the AI explanation."],
        ["Shock presets (4)", "Zone 1", "Set all seven inputs at once and run immediately: Concert in Town, Competitor −40%, Off-season Tuesday, Fully Booked Weekend."],
        ["Recommendation card", "Zone 2", "Recommended rate, uplift against current, P50 revenue with the P10–P90 range, expected occupancy, sell-out probability."],
        ["Accept price", "Zone 2", "Records the decision as accepted and saves the run."],
        ["Override", "Zone 2", "Lets the manager enter a different rate; the override is stored alongside the recommendation."],
        ["Multiplier chain", "Zone 2", "Shows every multiplier, the formula price and the revenue-maximised rate."],
        ["Forecast · next 14 days", "Zone 2", "Synthetic demand forecast with a widening confidence band."],
        ["Booking pace · pickup model", "Zone 2", "Expected versus actual share sold, with the pace index verdict."],
        ["Customer-side simulation", "Zone 2", "500-run revenue histogram with P10, P50, P90, conversion and segment split."],
        ["Comparison table", "Zone 2", "Current versus recommended versus matching the competitor on identical assumptions."],
        ["Guardrails panel", "Zone 3", "Any policy flag raised, with reason and mitigation."],
        ["AI explanation panel", "Zone 3", "Streaming rationale, risks and alternative strategy, with Skip and Re-generate."],
        ["Warning audit log tab", "Tab bar", "Timestamped compliance trail of every flag, with totals and refresh."],
        ["Presenter Mode", "Header", "Three-scenario guided walkthrough with auto-advance and zone spotlight."],
        ["Strategy Sheet", "Header", "Prints the one-page decision summary."],
        ["Reset", "Header", "Returns every input to the default night and clears the current result."],
    ],
    caption="Complete feature reference.",
    widths=[1.8, 0.9, 3.7],
)

# ============================ 13. ASSUMPTIONS ============================
pagebreak()
h1("12. Assumptions and limitations")
p("Stated plainly, so the simulator is not oversold in the room:")
bullets([
    ("Synthetic data.", "All demand history, forecasts and guest behaviour are generated from fixed random seeds. No "
     "real reservations, no real guests and no property management system data are involved."),
    ("One hotel, one room type.", "A single 100-room property with a ₹5,000 base rate. There is no room-type mix, no "
     "upgrade logic, no length-of-stay controls and no group or contracted business."),
    ("No live competitor feed.", "The competitor rate is a slider, not a scraped market rate. Real parity management "
     "would require an online travel agency or rate-shopping feed."),
    ("Static rules.", "The multipliers are fixed coefficients chosen for teaching clarity. A production system would "
     "estimate them from historical elasticity and refit them continuously."),
    ("Demand model, not demand truth.", "The logistic price-response curves are a modelling assumption. If the class "
     "disagrees with the leisure sensitivity, the recommendation changes — and that is the intended lesson."),
    ("Single night, no network effects.", "Displacement across dates, cancellations, no-shows, overbooking policy and "
     "ancillary revenue are all out of scope."),
    ("Flags do not block.", "No policy is enforced. Nothing in the tool can stop a manager accepting a flagged price."),
    ("No authentication.", "The application is an open classroom demo with no user accounts, roles or approval workflow."),
])

# ============================ 14. EXTENSIONS ============================
h1("13. Possible extensions")
table(
    ["Extension", "What it would add", "Main challenge"],
    [
        ["Multi-room-type and multi-property", "Rate structures across categories and a portfolio view with displacement between properties", "Cross-elasticity between room types and cannibalisation of upgrades"],
        ["Live competitor rates", "Real parity management from an online travel agency or rate-shopping feed", "Feed cost, rate-limits and matching the right competitor set"],
        ["Reinforcement learning agent", "A pricing policy learned from outcomes rather than hand-written multipliers", "Explainability and safe exploration — the agent must not experiment on real revenue"],
        ["Hard policy enforcement with sign-off", "Blocking flagged prices unless an authorised user approves, with a signed trail", "Requires authentication, roles and an approval workflow"],
        ["Guest booking portal", "Simulated guests actually booking at the published rate, closing the feedback loop", "Turning the Monte Carlo model into a live, stateful market"],
        ["Multi-night and length-of-stay controls", "Minimum stay rules and displacement analysis across a date range", "The optimisation becomes a horizon problem, not a single-night one"],
    ],
    caption="Extensions discussed as future work.",
    widths=[1.9, 2.5, 2.0],
)

# ============================ 15. GLOSSARY ============================
pagebreak()
h1("14. Glossary")
table(
    ["Term", "Meaning"],
    [
        ["ADR", "Average Daily Rate — average revenue earned per occupied room."],
        ["RevPAR", "Revenue per Available Room — occupancy multiplied by ADR; the headline measure of revenue management performance."],
        ["Occupancy", "Share of the hotel's rooms that are sold. In this tool, occupancy of remaining rooms is also reported separately."],
        ["Booking pace", "How fast a date is filling compared with the normal pickup curve for that number of days out."],
        ["Pickup", "New bookings received over a period; the pickup curve describes how a date normally fills over time."],
        ["Pace index", "Actual share sold divided by expected share sold. Above 1.0 is ahead of pace, below 0.9 is behind."],
        ["Lead time", "Days between the moment of booking and the arrival date."],
        ["Surge pricing", "Raising price sharply in response to a short-lived demand spike. Flagged here above 2.5× the base rate."],
        ["Rate parity", "Keeping rates consistent with the market and across distribution channels; large deviations affect conversion and ranking."],
        ["Fenced rate", "A discounted rate protected by conditions such as advance purchase or non-refundability, so it does not undercut full-rate demand."],
        ["Price elasticity / sensitivity (k)", "How sharply demand responds to a price change. High k means a small premium loses many bookings."],
        ["Reference price", "The price guests have been conditioned to expect for a night, blending the competitor rate, the base rate and the night's conditions."],
        ["Conversion rate", "Share of potential guests who actually book at a given price."],
        ["Monte Carlo simulation", "Running a scenario many times with random variation to obtain a distribution of outcomes instead of one estimate."],
        ["P10 / P50 / P90", "Percentiles of the simulated revenue distribution: the pessimistic case, the median and the optimistic case."],
        ["Multiplier chain", "The sequence of factors applied to the base rate to produce the formula price."],
        ["Variable cost", "Cost of servicing one occupied room (housekeeping, utilities, amenities). ₹1,200 here, and the absolute price floor."],
        ["Sell-out probability", "Share of simulated runs in which every remaining room was sold."],
        ["Perishable inventory", "Inventory that loses all value at a fixed moment — an unsold room tonight cannot be sold tonight again."],
        ["Shock scenario", "A preset that changes all scenario inputs at once to simulate a sudden market event."],
    ],
    caption="Glossary of revenue management and modelling terms used in this document.",
    widths=[1.8, 4.6],
)

doc.add_paragraph()
end = doc.add_paragraph()
end.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = end.add_run("— End of document —")
r.italic = True
r.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

os.makedirs(OUT_DIR, exist_ok=True)
doc.save(OUT)
print("written", OUT, os.path.getsize(OUT))
