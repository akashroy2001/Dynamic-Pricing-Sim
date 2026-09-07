import numpy as np
from datetime import datetime, timedelta, timezone

HOTEL = {
    "name": "The Grand Horizon Palace",
    "city": "Mumbai",
    "total_rooms": 100,
    "base_rate": 5000,
    "variable_cost": 1200,
    "currency": "INR",
    "occupancy_target": 0.75,
    "price_floor_mult": 0.2,
    "price_ceiling_mult": 3.0,
    "surge_warning_mult": 2.5,
    "fairness_gap_threshold": 0.5,
}

SEASON_PRICE_MULT = {"peak": 1.25, "shoulder": 1.00, "off": 0.80}
SEASON_DEMAND_MULT = {"peak": 1.20, "shoulder": 1.00, "off": 0.70}

SEGMENTS = {
    "leisure": {"share": 0.60, "sensitivity": 4.5, "base_conv": 0.55, "label": "Leisure (price-sensitive)"},
    "business": {"share": 0.40, "sensitivity": 1.8, "base_conv": 0.65, "label": "Business (time-sensitive)"},
}


def segment_sensitivity(seg_key: str, s: dict) -> float:
    if seg_key == "leisure":
        k = 4.5 + (1.0 if s["season"] == "off" else 0) - (1.0 if s["event_flag"] else 0)
    else:
        d = s["days_to_arrival"]
        k = 1.8 if d > 7 else 1.5 if d > 3 else 1.2
    return k

PRESETS = [
    {
        "id": "concert",
        "name": "Concert in Town",
        "tagline": "Stadium show, 40k visitors, city sells out",
        "scenario": {"demand_index": 175, "capacity_remaining_pct": 35, "days_to_arrival": 5, "season": "shoulder", "competitor_price": 8200, "event_flag": True, "current_price": 5000},
    },
    {
        "id": "competitor_cut",
        "name": "Competitor -40%",
        "tagline": "Rival across the road slashes rates overnight",
        "scenario": {"demand_index": 95, "capacity_remaining_pct": 60, "days_to_arrival": 10, "season": "shoulder", "competitor_price": 3000, "event_flag": False, "current_price": 5000},
    },
    {
        "id": "off_season",
        "name": "Off-season Tuesday",
        "tagline": "Monsoon midweek, lobby echoes",
        "scenario": {"demand_index": 45, "capacity_remaining_pct": 85, "days_to_arrival": 2, "season": "off", "competitor_price": 3800, "event_flag": False, "current_price": 5000},
    },
    {
        "id": "full_weekend",
        "name": "Fully Booked Weekend",
        "tagline": "Peak Saturday, six rooms left",
        "scenario": {"demand_index": 140, "capacity_remaining_pct": 6, "days_to_arrival": 1, "season": "peak", "competitor_price": 9500, "event_flag": False, "current_price": 5000},
    },
]


def lead_time_mult(days: int) -> float:
    if days <= 3:
        return 1.15
    if days <= 7:
        return 1.08
    if days <= 21:
        return 1.00
    return 0.93


def multipliers(s: dict) -> dict:
    base = HOTEL["base_rate"]
    r = s["capacity_remaining_pct"] / 100.0
    demand = float(np.clip(1 + 0.4 * (s["demand_index"] / 100.0 - 1), 0.65, 1.4))
    capacity = 1 + 0.5 * (1 - r) ** 2
    comp_ratio = s["competitor_price"] / base
    competitor = float(np.clip(1 + 0.3 * (comp_ratio - 1), 0.75, 1.25))
    return {
        "base_rate": base,
        "season": SEASON_PRICE_MULT[s["season"]],
        "demand": round(demand, 3),
        "capacity": round(capacity, 3),
        "competitor": round(competitor, 3),
        "lead_time": lead_time_mult(s["days_to_arrival"]),
        "event": 1.20 if s["event_flag"] else 1.0,
    }


def rule_price(m: dict) -> float:
    return m["base_rate"] * m["season"] * m["demand"] * m["capacity"] * m["competitor"] * m["lead_time"] * m["event"]


def reference_price(s: dict) -> float:
    r = s["capacity_remaining_pct"] / 100.0
    market = 0.5 * s["competitor_price"] + 0.5 * HOTEL["base_rate"]
    scarcity = 1 + 0.3 * (1 - r) ** 2
    urgency = 1.1 if s["days_to_arrival"] <= 3 else 1.0
    return market * 1.15 * SEASON_DEMAND_MULT[s["season"]] * (1.15 if s["event_flag"] else 1.0) * scarcity * urgency


def potential_demand(s: dict) -> float:
    rooms = HOTEL["total_rooms"] * s["capacity_remaining_pct"] / 100.0
    lead = 1.0 if s["days_to_arrival"] > 7 else 1.15
    return max(rooms, 8) * (s["demand_index"] / 100.0) * SEASON_DEMAND_MULT[s["season"]] * (1.25 if s["event_flag"] else 1.0) * lead


def segment_conversion(price: float, ref: float, seg: dict, k: float) -> float:
    return float(np.clip(seg["base_conv"] * 2 / (1 + np.exp(k * (price / ref - 1))), 0.02, 0.95))


def expected_outcome(price: float, s: dict) -> dict:
    rooms = HOTEL["total_rooms"] * s["capacity_remaining_pct"] / 100.0
    ref = reference_price(s)
    pot = potential_demand(s)
    seg_out, total = {}, 0.0
    for k, seg in SEGMENTS.items():
        conv = segment_conversion(price, ref, seg, segment_sensitivity(k, s))
        b = pot * seg["share"] * conv
        seg_out[k] = {"conversion": round(conv, 3), "bookings": round(b, 1)}
        total += b
    bookings = min(rooms, total)
    return {
        "price": round(price),
        "bookings": round(bookings, 1),
        "revenue": round(bookings * price),
        "occupancy_of_remaining": round(bookings / rooms, 3) if rooms > 0 else 0,
        "segments": seg_out,
    }


def segment_optimal_price(s: dict, seg_key: str, grid: np.ndarray) -> float:
    ref = reference_price(s)
    seg = SEGMENTS[seg_key]
    k = segment_sensitivity(seg_key, s)
    rev = [p * segment_conversion(p, ref, seg, k) for p in grid]
    return float(grid[int(np.argmax(rev))])


def optimize(s: dict) -> dict:
    m = multipliers(s)
    formula = rule_price(m)
    base = HOTEL["base_rate"]
    lo, hi = base * HOTEL["price_floor_mult"], base * HOTEL["price_ceiling_mult"]
    grid = np.arange(max(lo, formula * 0.7), min(hi, formula * 1.3) + 1, 50)
    outcomes = [expected_outcome(p, s) for p in grid]
    rooms = HOTEL["total_rooms"] * s["capacity_remaining_pct"] / 100.0
    target = HOTEL["occupancy_target"]
    feasible = [o for o in outcomes if o["occupancy_of_remaining"] >= target] or outcomes
    best = max(feasible, key=lambda o: o["revenue"])
    curve = [{"price": o["price"], "revenue": o["revenue"], "bookings": o["bookings"]} for o in outcomes[:: max(1, len(outcomes) // 24)]]

    full_grid = np.arange(lo, hi + 1, 100)
    seg_prices = {k: segment_optimal_price(s, k, full_grid) for k in SEGMENTS}
    warnings = build_warnings(best["price"], s, seg_prices)
    current = expected_outcome(s["current_price"], s)
    competitor = expected_outcome(s["competitor_price"], s)
    return {
        "recommended_price": best["price"],
        "formula_price": round(formula),
        "multipliers": m,
        "price_bounds": {"floor": round(lo), "ceiling": round(hi)},
        "expected": best,
        "current": current,
        "at_competitor_price": competitor,
        "revenue_curve": curve,
        "segment_optimal_prices": {k: round(v) for k, v in seg_prices.items()},
        "rooms_remaining": round(rooms),
        "occupancy_target": target,
        "constraint_binding": len([o for o in outcomes if o["occupancy_of_remaining"] >= target]) == 0,
        "warnings": warnings,
        "rules_used": [
            "Price = BaseRate × SeasonMult × DemandMult × CapacityMult × CompetitorAdj × LeadTimeMult × EventMult",
            "Grid search ±30% around formula price, step ₹50, maximise expected revenue",
            f"Constraint: expected occupancy of remaining rooms ≥ {int(target*100)}% (relaxed if infeasible)",
            f"Price bounds: {HOTEL['price_floor_mult']}× to {HOTEL['price_ceiling_mult']}× base rate",
            "Demand: logistic price-response per segment (Leisure k≈4.5 price-sensitive, Business k≈1.8 time-sensitive, tighter near arrival)",
        ],
    }


def build_warnings(price: float, s: dict, seg_prices: dict) -> list:
    w = []
    base, cost = HOTEL["base_rate"], HOTEL["variable_cost"]
    if price > HOTEL["surge_warning_mult"] * base:
        w.append({"code": "SURGE", "severity": "amber", "title": f"Surge {price/base:.1f}× base rate",
                  "detail": f"Recommended ₹{price:,.0f} exceeds the {HOTEL['surge_warning_mult']}× surge threshold. Reputational and regulatory exposure during events.",
                  "mitigation": "Cap at 2.5× or bundle value (breakfast, late checkout) to justify."})
    if price < cost:
        w.append({"code": "BELOW_COST", "severity": "amber", "title": "Price below variable cost",
                  "detail": f"₹{price:,.0f} is below the ₹{cost:,} variable cost per occupied room.",
                  "mitigation": "Hold at cost floor; accept lower occupancy rather than negative contribution."})
    gap = abs(seg_prices["business"] - seg_prices["leisure"]) / max(seg_prices["leisure"], 1)
    if gap > HOTEL["fairness_gap_threshold"]:
        w.append({"code": "FAIRNESS", "severity": "amber", "title": f"Segment price gap {gap*100:.0f}%",
                  "detail": f"Optimal Business rate ₹{seg_prices['business']:,.0f} vs Leisure ₹{seg_prices['leisure']:,.0f}. Differential pricing above {int(HOTEL['fairness_gap_threshold']*100)}% may be perceived as discriminatory.",
                  "mitigation": "Use fenced rates (advance-purchase, non-refundable) instead of segment-based pricing."})
    if price > 1.4 * s["competitor_price"]:
        w.append({"code": "PARITY", "severity": "amber", "title": "40%+ above competitor",
                  "detail": f"₹{price:,.0f} vs competitor ₹{s['competitor_price']:,.0f}. Leisure conversion will drop sharply; OTA ranking may suffer.",
                  "mitigation": "Monitor pickup daily; be ready to step down in ₹250 increments."})
    return w


def simulate(s: dict, price: float, iterations: int = 500, seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    rooms = int(round(HOTEL["total_rooms"] * s["capacity_remaining_pct"] / 100.0))
    ref = reference_price(s)
    pot = potential_demand(s)
    seg_bookings = {}
    total = np.zeros(iterations)
    for k, seg in SEGMENTS.items():
        conv = segment_conversion(price, ref, seg, segment_sensitivity(k, s))
        demand_noise = rng.lognormal(0, 0.2, iterations)
        arrivals = rng.poisson(np.maximum(pot * seg["share"] * demand_noise, 0.1))
        conv_noise = np.clip(conv * rng.normal(1, 0.12, iterations), 0.01, 0.98)
        b = rng.binomial(arrivals, conv_noise)
        seg_bookings[k] = b
        total += b
    bookings = np.minimum(total, rooms)
    revenue = bookings * price
    sold_before = HOTEL["total_rooms"] - rooms
    occupancy_final = (sold_before + bookings) / HOTEL["total_rooms"]
    counts, edges = np.histogram(revenue, bins=18)
    hist = [{"revenue": round(float((edges[i] + edges[i + 1]) / 2)), "count": int(counts[i])} for i in range(len(counts))]
    pot_total = max(pot, 1e-6)
    return {
        "iterations": iterations,
        "price": round(price),
        "revenue_p10": round(float(np.percentile(revenue, 10))),
        "revenue_p50": round(float(np.percentile(revenue, 50))),
        "revenue_p90": round(float(np.percentile(revenue, 90))),
        "revenue_mean": round(float(revenue.mean())),
        "bookings_mean": round(float(bookings.mean()), 1),
        "bookings_p10": round(float(np.percentile(bookings, 10)), 1),
        "bookings_p90": round(float(np.percentile(bookings, 90)), 1),
        "occupancy_final_mean": round(float(occupancy_final.mean()), 3),
        "occupancy_remaining_mean": round(float((bookings / max(rooms, 1)).mean()), 3),
        "conversion_rate": round(float((bookings.mean()) / pot_total), 3),
        "sellout_probability": round(float((total >= rooms).mean()), 3),
        "segments": {k: {"bookings_mean": round(float(v.mean()), 1), "share": round(float(v.mean() / max(total.mean(), 1e-6)), 3)} for k, v in seg_bookings.items()},
        "histogram": hist,
        "rooms_remaining": rooms,
    }


def forecast(seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=300)
    days = np.arange(365)
    dates = [start + timedelta(days=int(d)) for d in days]
    doy = np.array([d.timetuple().tm_yday for d in dates])
    seasonal = 100 * (1 + 0.28 * np.sin(2 * np.pi * (doy - 45) / 365) - 0.12 * np.cos(4 * np.pi * doy / 365))
    wd = np.array([d.weekday() for d in dates])
    weekday_eff = np.select([wd == 4, wd == 5, wd == 6, (wd == 1) | (wd == 2)], [1.15, 1.18, 0.90, 0.94], 1.0)
    noise = rng.normal(0, 6, 365)
    actual = np.clip(seasonal * weekday_eff + noise, 15, 220)
    series = [{"date": d.isoformat(), "demand": round(float(a), 1), "is_future": d > today} for d, a in zip(dates, actual)]
    fut_idx = [i for i, d in enumerate(dates) if today < d <= today + timedelta(days=14)]
    next14 = []
    for n, i in enumerate(fut_idx):
        f = float(seasonal[i] * weekday_eff[i])
        band = 4 + 1.2 * n
        next14.append({"date": dates[i].isoformat(), "day": dates[i].strftime("%a"), "forecast": round(f, 1), "low": round(f - band, 1), "high": round(f + band, 1)})
    tau = 12.0
    pace = [{"days_out": d, "expected_pct": round(100 * float(np.exp(-d / tau)), 1)} for d in range(60, -1, -2)]
    return {"today": today.isoformat(), "history": series, "next_14_days": next14, "pace_curve": pace, "pace_tau": tau}


def pace_status(s: dict) -> dict:
    tau = 12.0
    expected_pct = 100 * float(np.exp(-s["days_to_arrival"] / tau))
    actual_pct = 100 - s["capacity_remaining_pct"]
    return {"days_to_arrival": s["days_to_arrival"], "expected_sold_pct": round(expected_pct, 1), "actual_sold_pct": round(actual_pct, 1), "pace_index": round(actual_pct / max(expected_pct, 1), 2)}


def fallback_explanation(s: dict, opt: dict, sim: dict) -> dict:
    m = opt["multipliers"]
    drivers = sorted([(k, v) for k, v in m.items() if k != "base_rate"], key=lambda kv: abs(kv[1] - 1), reverse=True)[:3]
    driver_txt = ", ".join(f"{k.replace('_', ' ')} ×{v}" for k, v in drivers)
    delta = opt["expected"]["revenue"] - opt["current"]["revenue"]
    return {
        "why_this_price": f"The optimizer recommends ₹{opt['recommended_price']:,} (vs current ₹{s['current_price']:,}). The strongest drivers are {driver_txt}. At this rate the model expects {opt['expected']['bookings']} bookings from {opt['rooms_remaining']} remaining rooms, changing expected revenue by ₹{delta:,}.",
        "key_risks": [f"Revenue spread P10 ₹{sim['revenue_p10']:,} to P90 ₹{sim['revenue_p90']:,} — demand is uncertain.", f"Competitor at ₹{s['competitor_price']:,}; leisure guests are highly price-sensitive.", "Rule multipliers are static — real pickup may diverge from the forecast."],
        "alternative_strategy": "Hold the recommended rate for 48 hours, then re-run with observed pickup. If pace index drops below 0.9, step down in ₹250 increments; if above 1.2, step up.",
        "source": "fallback",
    }
