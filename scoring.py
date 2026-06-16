"""
Watch Score calculation for GameNight.

The default Watch Score blends several factor scores using fixed weights.
Each factor is on a 0–100 scale; the final score is rounded and capped at 0–100.
"""

from typing import Any

# Default weights for the Watch Score formula (must sum to 1.0).
WEIGHTS = {
    "offense": 0.20,
    "close_game": 0.20,
    "star_power": 0.20,
    "playoff_importance": 0.15,
    "rivalry": 0.10,
    "defense": 0.10,
    "accessibility": 0.05,
}

# Maps internal factor keys to the field names used in game data.
FACTOR_FIELDS = {
    "offense": "offense_score",
    "close_game": "close_game_score",
    "star_power": "star_power_score",
    "playoff_importance": "playoff_importance_score",
    "rivalry": "rivalry_score",
    "defense": "defense_score",
    "accessibility": "accessibility_score",
}

# Human-readable phrases used in the "why watch" explanation.
FACTOR_LABELS = {
    "offense": "strong offensive matchups",
    "close_game": "a high chance of being close",
    "star_power": "strong star power",
    "playoff_importance": "significant playoff implications",
    "rivalry": "a historic rivalry",
    "defense": "elite defensive play",
    "accessibility": "easy access on a major network",
}


def _get_factor_value(game: dict[str, Any], factor_key: str) -> float:
    """Read a factor score from a game dict, defaulting to 0 if missing."""
    field_name = FACTOR_FIELDS[factor_key]
    return float(game.get(field_name, 0))


def calculate_watch_score(game: dict[str, Any]) -> int:
    """
    Calculate the weighted Watch Score for a game.

    Formula (each factor is 0–100):
        watch_score = offense×20% + close_game×20% + star_power×20%
                    + playoff_importance×15% + rivalry×10% + defense×10%
                    + accessibility×5%

    The result is rounded to the nearest whole number and capped between 0 and 100.
    """
    total = 0.0
    for factor_key, weight in WEIGHTS.items():
        total += _get_factor_value(game, factor_key) * weight

    rounded = round(total)
    return max(0, min(100, rounded))


def build_score_breakdown(game: dict[str, Any]) -> dict[str, Any]:
    """
    Build a detailed breakdown showing each factor's score, weight,
    and weighted contribution to the final Watch Score.
    """
    breakdown: dict[str, Any] = {}

    for factor_key, weight in WEIGHTS.items():
        score = _get_factor_value(game, factor_key)
        breakdown[factor_key] = {
            "score": int(score),
            "weight": weight,
            "weighted_contribution": round(score * weight, 2),
        }

    breakdown["watch_score"] = calculate_watch_score(game)
    return breakdown


def generate_why_watch(game: dict[str, Any], top_n: int = 2) -> str:
    """
    Create a short explanation highlighting the game's strongest factors.

    Picks the top factor scores and turns them into a readable sentence.
    Example: "This game ranks highly because of strong star power and
    a high chance of being close."
    """
    # Rank factors by their raw scores (highest first).
    ranked = sorted(
        FACTOR_FIELDS.keys(),
        key=lambda key: _get_factor_value(game, key),
        reverse=True,
    )

    top_factors = ranked[:top_n]
    labels = [FACTOR_LABELS[key] for key in top_factors]

    if len(labels) == 1:
        reason_text = labels[0]
    elif len(labels) == 2:
        reason_text = f"{labels[0]} and {labels[1]}"
    else:
        reason_text = ", ".join(labels[:-1]) + f", and {labels[-1]}"

    return f"This game ranks highly because of {reason_text}."


def enrich_game(game: dict[str, Any]) -> dict[str, Any]:
    """
    Add computed watch_score and why_watch fields to a raw game dict.
    """
    enriched = dict(game)
    enriched["watch_score"] = calculate_watch_score(game)
    enriched["why_watch"] = generate_why_watch(game)
    return enriched
