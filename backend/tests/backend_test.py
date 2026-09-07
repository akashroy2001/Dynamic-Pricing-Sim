"""Backend API tests for Hotel Dynamic Pricing Simulator."""
import os
import time
import pytest
import requests

BASE = os.environ["REACT_APP_BACKEND_URL"].rstrip("/") if os.environ.get("REACT_APP_BACKEND_URL") else None
if not BASE:
    # fallback: read frontend .env
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                BASE = line.split("=", 1)[1].strip().rstrip("/")

API = f"{BASE}/api"


@pytest.fixture(scope="module")
def presets():
    r = requests.get(f"{API}/config", timeout=30)
    assert r.status_code == 200
    data = r.json()
    return {p["id"]: p["scenario"] for p in data["presets"]}


# --- /api/config ---
def test_config():
    r = requests.get(f"{API}/config", timeout=30)
    assert r.status_code == 200
    d = r.json()
    assert "hotel" in d and "segments" in d and "presets" in d and "default_scenario" in d
    ids = {p["id"] for p in d["presets"]}
    assert ids == {"concert", "competitor_cut", "off_season", "full_weekend"}


# --- /api/forecast ---
def test_forecast():
    r = requests.get(f"{API}/forecast", timeout=30)
    assert r.status_code == 200
    d = r.json()
    assert len(d["history"]) == 365
    assert len(d["next_14_days"]) == 14
    assert all("forecast" in x and "low" in x and "high" in x for x in d["next_14_days"])
    assert isinstance(d["pace_curve"], list) and len(d["pace_curve"]) > 0


# --- /api/pace ---
def test_pace(presets):
    r = requests.post(f"{API}/pace", json=presets["concert"], timeout=30)
    assert r.status_code == 200
    d = r.json()
    for k in ("pace_index", "expected_sold_pct", "actual_sold_pct"):
        assert k in d


# --- /api/optimize ---
def test_optimize(presets):
    r = requests.post(f"{API}/optimize", json=presets["concert"], timeout=30)
    assert r.status_code == 200
    d = r.json()
    lo, hi = d["price_bounds"]["floor"], d["price_bounds"]["ceiling"]
    assert lo <= d["recommended_price"] <= hi
    assert "multipliers" in d and "warnings" in d and "expected" in d and "rules_used" in d


def test_optimize_validation():
    bad = {"demand_index": 100, "capacity_remaining_pct": 60, "days_to_arrival": 14, "season": "spring", "competitor_price": 5000, "event_flag": False, "current_price": 5000}
    r = requests.post(f"{API}/optimize", json=bad, timeout=30)
    assert r.status_code == 422


# --- /api/simulate ---
def test_simulate(presets):
    payload = {"scenario": presets["concert"], "price": 8000, "iterations": 500}
    r = requests.post(f"{API}/simulate", json=payload, timeout=30)
    assert r.status_code == 200
    d = r.json()
    assert d["revenue_p10"] <= d["revenue_p50"] <= d["revenue_p90"]
    assert 0 <= d["occupancy_final_mean"] <= 1
    assert isinstance(d["histogram"], list) and len(d["histogram"]) > 0


# --- /api/recommend ---
def test_recommend_full_weekend_surge(presets):
    r = requests.post(f"{API}/recommend", json=presets["full_weekend"], timeout=45)
    assert r.status_code == 200
    d = r.json()
    for k in ("optimization", "simulation", "simulation_current", "simulation_competitor", "pace"):
        assert k in d
    codes = [w["code"] for w in d["optimization"]["warnings"]]
    assert "SURGE" in codes, f"expected SURGE, got {codes}"


def test_recommend_off_season_fairness(presets):
    r = requests.post(f"{API}/recommend", json=presets["off_season"], timeout=45)
    assert r.status_code == 200
    codes = [w["code"] for w in r.json()["optimization"]["warnings"]]
    assert "FAIRNESS" in codes, f"expected FAIRNESS, got {codes}"


def test_recommend_validation():
    bad = {"demand_index": 100, "capacity_remaining_pct": 60, "days_to_arrival": 14, "season": "winter", "competitor_price": 5000, "event_flag": False, "current_price": 5000}
    r = requests.post(f"{API}/recommend", json=bad, timeout=30)
    assert r.status_code == 422


# --- /api/explain ---
def test_explain_and_cache(presets):
    scenario = presets["concert"]
    rec = requests.post(f"{API}/recommend", json=scenario, timeout=45).json()
    payload = {"scenario": scenario, "optimization": rec["optimization"], "simulation": rec["simulation"]}
    r1 = requests.post(f"{API}/explain", json=payload, timeout=60)
    assert r1.status_code == 200
    d1 = r1.json()
    for k in ("why_this_price", "key_risks", "alternative_strategy", "source", "cached"):
        assert k in d1
    assert isinstance(d1["key_risks"], list)
    assert d1["source"] in ("gemini-3-flash", "fallback")
    print(f"EXPLAIN source={d1['source']}")
    # Second identical call should be cached
    r2 = requests.post(f"{API}/explain", json=payload, timeout=30)
    assert r2.status_code == 200
    assert r2.json()["cached"] is True


# --- /api/runs ---
def test_runs_create_and_list(presets):
    scenario = presets["concert"]
    rec = requests.post(f"{API}/recommend", json=scenario, timeout=45).json()
    run = {
        "label": "TEST_run",
        "scenario": scenario,
        "optimization": rec["optimization"],
        "simulation": rec["simulation"],
        "decision": "accepted",
    }
    r = requests.post(f"{API}/runs", json=run, timeout=30)
    assert r.status_code == 200
    rid = r.json()["id"]
    lst = requests.get(f"{API}/runs?limit=20", timeout=30).json()
    assert any(x["id"] == rid for x in lst)
    match = [x for x in lst if x["id"] == rid][0]
    assert match["recommended_price"] == rec["optimization"]["recommended_price"]
    assert match["decision"] == "accepted"
