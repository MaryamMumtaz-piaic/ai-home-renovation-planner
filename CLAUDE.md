# CLAUDE.md

Guidance for Claude Code (or any AI agent) working in this repository.

## What this is

AI Home Renovation Planner — a FastAPI + Jinja2 + Tailwind + vanilla-JS web app where a pipeline of OpenAI-backed agents turns a user's room/budget/style input into a structured renovation plan. Full original product spec lives in `task.md` at the repo root — read it before making product-level decisions.

## Running it

```bash
pip install -r requirements.txt
copy .env.example .env   # fill in OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

No database, no auth, no build step. Saved projects live in the browser's `localStorage`; reference data (materials, inspiration, room types, design styles) lives in `app/data/*.json`.

## Architecture rules to preserve

- **All OpenAI calls go through `app/services/openai_service.py`.** Never call the OpenAI SDK from a route or agent file directly — routes call agents, agents call `openai_service`.
- **Every agent returns a validated Pydantic model**, never raw text. `openai_service` validates, retries once on a bad response, then raises `AIGenerationError` rather than returning unvalidated data. Routes catch `AIGenerationError` → HTTP 502 and `ValueError` (incomplete input) → HTTP 400.
- **The orchestrator (`app/agents/orchestrator.py`) owns sequencing**, not the routes. It runs independent agents concurrently (`asyncio.gather`) and only re-runs the specific agents a critic issue implicates, not the whole pipeline.
- **`app/services/json_store.py` is the only place that reads/writes `app/data/*.json`.** Don't duplicate file I/O elsewhere.
- Model field names in `app/models/renovation.py` are the source of truth for JSON payload shapes shared between backend and frontend (`static/js/*.js` builds/reads these same field names) — if you rename a field, update both sides and the templates that render it.

## Product boundaries (do not relax without being asked)

- Never present AI output as a contractor quotation, architectural drawing, or engineering approval — always framed as a planning estimate.
- Never give step-by-step DIY instructions for electrical, gas, structural, major plumbing, or roofing work — recommend a qualified professional instead.
- Never fabricate live market prices or supplier data as if real-time.

## Conventions

- Python: full type hints, async/await for I/O and AI calls, Pydantic v2.
- Frontend: no frameworks, no bundler — plain `<script>` includes, Tailwind CDN + `static/css/styles.css` for the custom design system (warm/editorial palette — see section 6-7 of `task.md`).
- Keep AI prompts minimal: pass only the fields a given agent actually needs, not the whole brief/plan object (see `task.md` section 62).
