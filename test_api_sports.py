"""Quick manual test for API-SPORTS (uses 2 of your daily requests)."""

import asyncio
import json

from api_sports_client import ApiSportsError, get_games, get_leagues


async def main() -> None:
    # Matches dashboard: GET /games?date=YYYY-MM-DD
    # Free plan only allows a short recent window (API tells you in errors).
    test_date = "2026-06-22"

    print(f"Fetching games for {test_date} (GET /games?date=...)...")
    try:
        games = await get_games(date=test_date)
        count = games.get("results", 0)
        print(f"  {count} games returned")
        if count:
            first = games["response"][0]
            home = first["teams"]["home"]["name"]
            away = first["teams"]["away"]["name"]
            league = first["league"]["name"]
            print(f"  First game: {away} @ {home} ({league})")
        print(json.dumps(games, indent=2))
    except ApiSportsError as exc:
        print(f"  Games request failed: {exc}")

    print("\nFetching leagues...")
    leagues = await get_leagues()
    print(f"  {leagues.get('results', 0)} leagues returned")


if __name__ == "__main__":
    asyncio.run(main())
