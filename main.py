from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import FactorBreakdown, Game, GameDetail, GamesResponse, HealthResponse, ScoreBreakdown
from sample_data import SAMPLE_GAMES
from scoring import build_score_breakdown, enrich_game

app = FastAPI(
    title="GameNight API",
    description="Backend for GameNight — find the best games to watch tonight.",
    version="0.1.0",
)

# Allow the frontend to call this API from localhost during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_games() -> list[dict]:
    """Load sample games with computed watch_score and why_watch."""
    return [enrich_game(game) for game in SAMPLE_GAMES]


def _build_game_detail(game: dict) -> GameDetail:
    """Build a GameDetail response including the full score breakdown."""
    raw_breakdown = build_score_breakdown(game)

    score_breakdown = ScoreBreakdown(
        offense=FactorBreakdown(**raw_breakdown["offense"]),
        close_game=FactorBreakdown(**raw_breakdown["close_game"]),
        star_power=FactorBreakdown(**raw_breakdown["star_power"]),
        playoff_importance=FactorBreakdown(**raw_breakdown["playoff_importance"]),
        rivalry=FactorBreakdown(**raw_breakdown["rivalry"]),
        defense=FactorBreakdown(**raw_breakdown["defense"]),
        accessibility=FactorBreakdown(**raw_breakdown["accessibility"]),
        watch_score=raw_breakdown["watch_score"],
    )

    return GameDetail(score_breakdown=score_breakdown, **game)


@app.get("/api/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Simple health check for load balancers and local dev."""
    return HealthResponse(status="ok", message="GameNight API is running")


@app.get("/api/games", response_model=GamesResponse)
def list_games() -> GamesResponse:
    """Return all sample NBA games sorted by Watch Score (highest first)."""
    games = sorted(_load_games(), key=lambda g: g["watch_score"], reverse=True)
    return GamesResponse(count=len(games), games=[Game(**g) for g in games])


@app.get("/api/games/{game_id}", response_model=GameDetail)
def get_game(game_id: str) -> GameDetail:
    """Return one game by ID with a full Watch Score breakdown."""
    for raw_game in SAMPLE_GAMES:
        if raw_game["id"] == game_id:
            enriched = enrich_game(raw_game)
            return _build_game_detail(enriched)

    raise HTTPException(status_code=404, detail=f"Game not found: {game_id}")
