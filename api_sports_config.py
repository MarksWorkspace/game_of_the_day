"""
API-SPORTS configuration for GameNight.

Docs: https://api-sports.io/documentation

Free tier: 100 requests/day — cache responses and avoid calling the API on every
page load.
"""

from dataclasses import dataclass
from enum import Enum


class ApiSport(str, Enum):
    """Supported API-SPORTS base URLs."""

    BASEBALL = "https://v1.baseball.api-sports.io"
    BASKETBALL = "https://v1.basketball.api-sports.io"


DEFAULT_SPORT = ApiSport.BASEBALL

API_KEY_HEADER = "x-apisports-key"

DAILY_REQUEST_LIMIT = 100

# Common baseball league names → API-SPORTS league IDs (for direct API calls).
BASEBALL_LEAGUES: dict[str, int] = {
    "MLB": 1,
    "LMB": 21,
    "NPB": 2,
    "KBO": 3,
}

# Free plan only allows recent dates (API returns the valid window in errors).
# Example: "try from 2026-06-21 to 2026-06-23"


@dataclass(frozen=True)
class Endpoint:
    path: str
    method: str = "GET"
    description: str = ""


ENDPOINTS = {
    "leagues": Endpoint(
        path="/leagues",
        description="List available leagues.",
    ),
    "games": Endpoint(
        path="/games",
        description="Games for a date, league, team, or id.",
    ),
    "games_h2h": Endpoint(
        path="/games/h2h",
        description="Head-to-head games between two teams.",
    ),
}


GAMES_PARAMS = {
    "id": {"required": False, "type": "integer", "description": "Game ID."},
    "date": {
        "required": False,
        "type": "string",
        "format": "YYYY-MM-DD",
        "example": "2024-08-22",
        "description": "Games on a specific date.",
    },
    "league": {"required": False, "type": "integer", "description": "League ID."},
    "season": {"required": False, "type": "integer", "description": "Season year."},
    "team": {"required": False, "type": "integer", "description": "Team ID."},
    "timezone": {"required": False, "type": "string", "description": "Valid timezone."},
}


GAMES_H2H_PARAMS = {
    "h2h": {
        "required": True,
        "type": "string",
        "format": "{team_id}-{team_id}",
        "example": "5-6",
        "description": "Two team IDs separated by a hyphen.",
    },
    "date": {
        "required": False,
        "type": "string",
        "format": "YYYY-MM-DD",
        "example": "2017-04-28",
        "description": "Filter games on a specific date.",
    },
    "league": {
        "required": False,
        "type": "integer",
        "description": "League ID.",
    },
    "season": {
        "required": False,
        "type": "integer",
        "format": "4 characters",
        "description": "Season year (e.g. 2024).",
    },
    "timezone": {
        "required": False,
        "type": "string",
        "description": "Valid timezone (e.g. America/New_York).",
    },
}
