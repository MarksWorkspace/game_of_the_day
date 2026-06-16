from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FactorBreakdown(BaseModel):
    """How one scoring factor contributed to the Watch Score."""

    score: int = Field(..., ge=0, le=100, description="Raw factor score (0–100)")
    weight: float = Field(..., description="Weight used in the formula (e.g. 0.20 = 20%)")
    weighted_contribution: float = Field(
        ..., description="score × weight before rounding the final Watch Score"
    )


class ScoreBreakdown(BaseModel):
    """Full breakdown of how the Watch Score was calculated."""

    offense: FactorBreakdown
    close_game: FactorBreakdown
    star_power: FactorBreakdown
    playoff_importance: FactorBreakdown
    rivalry: FactorBreakdown
    defense: FactorBreakdown
    accessibility: FactorBreakdown
    watch_score: int = Field(..., ge=0, le=100)


class Game(BaseModel):
    """A single NBA game with factor scores and computed Watch Score."""

    id: str
    league: str
    home_team: str
    away_team: str
    start_time: datetime
    network: str
    offense_score: int = Field(..., ge=0, le=100)
    defense_score: int = Field(..., ge=0, le=100)
    star_power_score: int = Field(..., ge=0, le=100)
    close_game_score: int = Field(..., ge=0, le=100)
    rivalry_score: int = Field(..., ge=0, le=100)
    playoff_importance_score: int = Field(..., ge=0, le=100)
    accessibility_score: int = Field(..., ge=0, le=100)
    watch_score: int = Field(..., ge=0, le=100)
    why_watch: str


class GameDetail(Game):
    """Single-game response with the full score breakdown."""

    score_breakdown: ScoreBreakdown


class HealthResponse(BaseModel):
    status: str
    message: str


class GamesResponse(BaseModel):
    count: int
    games: list[Game]
