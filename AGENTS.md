# AGENTS.md

Instructions for AI coding agents (Codex, Cursor, Copilot Workspace, Claude, etc.) contributing to this repository. See `CLAUDE.md` for Claude-Code-specific notes and `task.md` for the full original product specification.

## Setup

```bash
pip install -r requirements.txt
copy .env.example .env   # set OPENAI_API_KEY; OPENAI_MODEL defaults to gpt-4.1-mini
uvicorn app.main:app --reload --port 8000
```

## Project layout

```
app/main.py            FastAPI entrypoint
app/routes/             HTTP routes (pages + JSON APIs)
app/agents/              one module per planning agent + orchestrator.py
app/services/            openai_service.py (all AI calls), json_store.py, pdf_service.py
app/models/               Pydantic models — the contract between backend and frontend
app/data/                 JSON reference data (materials, inspiration, room types, styles)
app/utils/                validation/scoring/formatting helpers
templates/                Jinja2 HTML, extends base.html
static/css/styles.css     hand-built design system (used alongside Tailwind CDN utilities)
static/js/                 vanilla JS, one file per page area + main.js (shared)
```

## Rules

1. **Don't call the OpenAI SDK outside `app/services/openai_service.py`.** Agents in `app/agents/` call functions in that service; they don't construct clients or prompts inline.
2. **Don't skip validation.** Every AI response must be parsed into its Pydantic model before use. On failure, retry once, then raise `AIGenerationError` — never pass raw model text up to a route or template.
3. **Don't run agents you don't need.** The orchestrator decides what runs and in what order based on real data dependencies (see the DAG comment in `app/agents/orchestrator.py`). A revision pass after a critic finding should re-run only the implicated agents.
4. **Don't duplicate JSON file I/O.** Use `app/services/json_store.py`.
5. **Keep model field names and JSON shapes in sync across three places** when you change them: `app/models/renovation.py`, the template that renders the field, and the JS file that reads/writes it (`static/js/plan.js` / `planner.js` mainly).
6. **No new backend infra.** No database, no auth, no separate frontend server, no additional services beyond what's already here — this is intentionally a single FastAPI process serving everything.
7. **Respect the safety framing.** Renovation plans are estimates, not professional deliverables; high-risk work (electrical/gas/structural/plumbing/roofing) gets a "consult a professional" note, not instructions.
8. **Frontend stays framework-free.** Plain HTML/Jinja2, Tailwind CDN utility classes plus `static/css/styles.css` for the custom design system, vanilla JS with defensive `null` checks (JS files are shared across pages that may not contain every element they reference).

## Testing a change end-to-end

1. Start the server, walk the planner flow (`/planner`) for at least one room type through to plan generation.
2. Confirm the generated plan renders fully on the plan page (budget chart, shopping list, timeline, execution checklist).
3. Exercise Adapt Plan and What-If on that plan.
4. Save the project, reload `/projects`, confirm it appears and reopens correctly.
5. Check `/materials`, `/inspiration`, `/contact`, `/faq`, and a 404 route still work.
