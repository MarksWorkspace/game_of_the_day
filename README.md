# GameNight Backend

Backend API for **GameNight** — helps sports fans answer: *"What are the best games to watch tonight?"*

This MVP serves sample NBA game data and calculates a default **Watch Score** for each game.

## Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- Sample in-memory data (SQLite / real sports API coming later)

## Quick start (easiest)

**Windows — double-click or run from terminal:**

```powershell
.\run.bat
```

Or in PowerShell:

```powershell
.\run.ps1
```

This creates the virtual environment if needed, installs dependencies, opens the API docs in your browser, and starts the server at `http://127.0.0.1:8000` (or `8080` if port 8000 is already in use).

## Setup (manual)

### 1. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI server

```bash
python -m uvicorn main:app --reload
```

Or use `.\run.bat` / `.\run.ps1` instead (recommended on Windows).

The API will be available at `http://127.0.0.1:8000`.

### 4. Open the interactive API docs

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/games` | All sample NBA games, sorted by Watch Score (highest first) |
| `GET` | `/api/games/{game_id}` | One game by ID with full score breakdown |

### Example responses

**Health check**

```bash
curl http://127.0.0.1:8000/api/health
```

**List games**

```bash
curl http://127.0.0.1:8000/api/games
```

**Single game**

```bash
curl http://127.0.0.1:8000/api/games/nba-2026-06-15-lal-bos
```

## Watch Score Formula

Each game has factor scores from 0–100. The default Watch Score is a weighted average:

| Factor | Weight |
|--------|--------|
| Offense | 20% |
| Close game likelihood | 20% |
| Star power | 20% |
| Playoff importance | 15% |
| Rivalry | 10% |
| Defense | 10% |
| Network / accessibility | 5% |

The score is rounded to the nearest whole number and capped between 0 and 100.

## Project Structure

```
main.py          # FastAPI app and routes
models.py        # Pydantic response models
sample_data.py   # Sample NBA games
scoring.py       # Watch Score calculation and "why watch" text
requirements.txt # Python dependencies
README.md        # This file
```

## CORS

CORS is enabled for common local frontend dev ports (`localhost:3000`, `localhost:5173`).

## API-SPORTS integration

Baseball API client files:

- `api_sports_config.py` — base URLs, endpoints, parameter docs
- `api_sports_client.py` — async `get_leagues()` and `get_games_h2h()` helpers

Setup:

1. Copy `.env.example` to `.env` and add your key:
   ```
   APISPORTS_KEY=your_api_key_here
   ```
2. Free tier is **100 requests/day** — cache responses when you wire this into routes.

Test (uses 2 API requests):

```powershell
python test_api_sports.py
```

## What's Not Included Yet

- Authentication
- Real database (SQLite)
- Live sports data wired into `/api/games` (client is ready)
