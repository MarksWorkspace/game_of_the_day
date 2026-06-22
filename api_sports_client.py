"""
Async client for API-SPORTS.

Loads the API key from the APISPORTS_KEY environment variable (.env supported).

Example:
    from api_sports_client import get_games, get_leagues, get_games_h2h

    games = await get_games(date="2024-08-22")
    leagues = await get_leagues()
    h2h = await get_games_h2h(h2h="5-6", date="2017-04-28")
"""

import os
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

from api_sports_config import API_KEY_HEADER, DEFAULT_SPORT, ENDPOINTS, ApiSport

load_dotenv()


class ApiSportsError(Exception):
    """Raised when the API returns errors or the request fails."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        errors: list | dict | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.errors = errors or []

    def __str__(self) -> str:
        base = super().__str__()
        if self.errors:
            return f"{base}: {self.errors}"
        return base


def _get_api_key() -> str:
    key = os.getenv("APISPORTS_KEY", "").strip()
    if not key:
        raise ApiSportsError(
            "Missing APISPORTS_KEY. Add it to a .env file in the project root."
        )
    return key


async def _request(
    path: str,
    *,
    sport: ApiSport = DEFAULT_SPORT,
    params: Optional[dict[str, Any]] = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Send one GET request to API-SPORTS and return the parsed JSON body."""
    url = f"{sport.value}{path}"
    headers = {API_KEY_HEADER: _get_api_key()}

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code >= 400:
        raise ApiSportsError(
            f"API-SPORTS request failed: {response.status_code} {response.reason_phrase}",
            status_code=response.status_code,
        )

    data = response.json()
    errors = data.get("errors")
    if errors:
        raise ApiSportsError(
            "API-SPORTS returned errors",
            status_code=response.status_code,
            errors=errors,
        )

    return data


async def get_leagues(*, sport: ApiSport = DEFAULT_SPORT) -> dict[str, Any]:
    """GET /leagues — list available leagues."""
    return await _request(ENDPOINTS["leagues"].path, sport=sport)


async def get_games(
    *,
    game_id: Optional[int] = None,
    date: Optional[str] = None,
    league: Optional[int] = None,
    season: Optional[int] = None,
    team: Optional[int] = None,
    timezone: Optional[str] = None,
    sport: ApiSport = DEFAULT_SPORT,
) -> dict[str, Any]:
    """
    GET /games — games by date, league, team, or id.

    Matches the dashboard call: /games?date=2024-08-22
    """
    params: dict[str, Any] = {}

    if game_id is not None:
        params["id"] = game_id
    if date is not None:
        params["date"] = date
    if league is not None:
        params["league"] = league
    if season is not None:
        params["season"] = season
    if team is not None:
        params["team"] = team
    if timezone is not None:
        params["timezone"] = timezone

    return await _request(ENDPOINTS["games"].path, sport=sport, params=params)


async def get_games_h2h(
    h2h: str,
    *,
    date: Optional[str] = None,
    league: Optional[int] = None,
    season: Optional[int] = None,
    timezone: Optional[str] = None,
    sport: ApiSport = DEFAULT_SPORT,
) -> dict[str, Any]:
    """
    GET /games/h2h — head-to-head games between two teams.

    Args:
        h2h: Team IDs as "id-id" (e.g. "5-6").
        date: Optional YYYY-MM-DD filter.
        league: Optional league ID.
        season: Optional season year (e.g. 2024).
        timezone: Optional timezone string.
    """
    params: dict[str, Any] = {"h2h": h2h}

    if date is not None:
        params["date"] = date
    if league is not None:
        params["league"] = league
    if season is not None:
        params["season"] = season
    if timezone is not None:
        params["timezone"] = timezone

    return await _request(ENDPOINTS["games_h2h"].path, sport=sport, params=params)
