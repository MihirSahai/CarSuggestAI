from typing import List, Dict, Any, Optional
from dataclasses import dataclass


# -----------------------------
# Config / Weights
# -----------------------------

DEFAULT_WEIGHTS = {
    "safety": 0.25,
    "comfort": 0.15,
    "mileage": 0.15,
    "features": 0.15,
    "performance": 0.15,
    "reliability": 0.15,
}


# -----------------------------
# Utility normalization
# -----------------------------

def normalize_price_diff(budget: float, price: float) -> float:
    """
    Returns score between 0 and 1.
    Penalizes cars above budget.
    """
    if budget <= 0:
        return 0

    if price <= budget:
        return 1.0

    # exponential penalty beyond budget
    diff_ratio = (price - budget) / budget
    return max(0.0, 1.0 - diff_ratio)


# -----------------------------
# Hard Filtering
# -----------------------------

def apply_filters(cars: List[Dict], intent: Dict[str, Any]) -> List[Dict]:
    """
    Deterministic filtering based on constraints.
    """

    filtered = cars

    budget = intent.get("budget")
    fuel_type = intent.get("fuel_type")
    seating = intent.get("seating")
    segment = intent.get("segment") 

    if segment:
        if segment.lower() in car["segment"].lower():
            score += 2.5   # strong boost
        else:
            score -= 1.5   # mild penalty

    if budget:
        # filtered = [c for c in filtered if c["price_lakh"] <= budget * 1.2]
        # allow 20% buffer
        filtered = sorted(filtered, key=lambda x: abs(x["price_lakh"] - budget))

    if fuel_type:
        filtered = [
            c for c in filtered
            if fuel_type.lower() in c["fuel_type"].lower()
        ]

    if seating:
        filtered = [
            c for c in filtered
            if c["seating"] >= seating
        ]

    return filtered


# -----------------------------
# Scoring Engine
# -----------------------------

def score_car(car: Dict, intent: Dict[str, Any], weights: Dict[str, float]) -> float:
    """
    Weighted deterministic scoring function.
    """

    budget = intent.get("budget", 0)

    score = 0.0

    # core attributes
    score += car["safety"] * weights["safety"]
    score += car["comfort"] * weights["comfort"]
    score += car["mileage"] * weights["mileage"]
    score += car["features"] * weights["features"]
    score += car["performance"] * weights["performance"]
    score += car["reliability"] * weights["reliability"]

    # budget fit adjustment (very important signal)
    budget_score = normalize_price_diff(budget, car["price_lakh"])
    score += budget_score * 2.0  # strong multiplier

    # preference boosts (optional intent signals)
    priorities = intent.get("priorities", [])

    if "safety" in priorities:
        score += car["safety"] * 0.3

    if "mileage" in priorities:
        score += car["mileage"] * 0.3

    if "performance" in priorities:
        score += car["performance"] * 0.3

    if "comfort" in priorities:
        score += car["comfort"] * 0.3

    return round(score, 4)


# -----------------------------
# Ranking Engine
# -----------------------------

def rank_cars(cars: List[Dict], intent: Dict[str, Any]) -> List[Dict]:
    """
    Attach score and sort.
    """

    weights = intent.get("weights", DEFAULT_WEIGHTS)

    scored = []

    for car in cars:
        score = score_car(car, intent, weights)
        car_copy = car.copy()
        car_copy["score"] = score
        scored.append(car_copy)

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored


# -----------------------------
# Top-K Selector
# -----------------------------

def select_top_k(cars: List[Dict], k: int = 5) -> List[Dict]:
    return cars[:k]


# -----------------------------
# MAIN PIPELINE
# -----------------------------

def recommend_cars(
    cars: List[Dict],
    intent: Dict[str, Any],
    top_k: int = 5
) -> List[Dict]:
    """
    Full deterministic recommendation pipeline.
    """

    # 1. Filter
    filtered = apply_filters(cars, intent)

    # edge case: fallback if filtering too strict
    if not filtered:
        filtered = cars

    # 2. Rank
    ranked = rank_cars(filtered, intent)

    # 3. Top-K
    return select_top_k(ranked, top_k)