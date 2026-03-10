# Donation Tracker Backend

Live donation scraper & API for the **UB ISoc Gaza Appeal** (Mercy Relief).

## Setup & Run

```bash
pip install -r requirements.txt
python main.py
```

Server starts at: `http://localhost:8000`

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/donations` | Live donation total + milestone data |
| `GET /health` | Scraper health status |
| `GET /docs` | Auto-generated Swagger UI |

## Example Response

```json
{
  "current_total": 1375.0,
  "next_target": 2000,
  "progress_percent": 68.75,
  "remaining": 625.0,
  "last_updated": "2026-03-09T20:10:00"
}
```

## Milestones

`250 → 500 → 1000 → 2000 → 3000 → 4000 → 5000 → 6000 → 7000 → 8000 → 10000 → 15000 → 20000`

## Project Structure

```
donation-tracker-backend/
├── main.py          # Entry point — starts scraper + API server
├── scraper.py       # Background scraper (runs every 30s)
├── api.py           # FastAPI routes
├── milestones.py    # Milestone calculation logic
└── requirements.txt
```

## Notes

- The scraper uses multiple CSS selector strategies + a regex fallback to locate the donation total. If the page layout changes, check `scraper.py → parse_total_from_html()`.
- CORS is open (`allow_origins=["*"]`) so any frontend can call the API.
- The cached value is served instantly; scraping happens in a background thread.
