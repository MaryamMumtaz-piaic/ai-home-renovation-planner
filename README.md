# AI Home Renovation Planner

A premium, AI-powered renovation planning platform. Describe a room, your goals, budget, and style — a pipeline of specialized AI agents turns that into a complete renovation plan: design concept, space plan, budget breakdown, material recommendations, shopping list, timeline, and an execution checklist.

This is not a chatbot, not an image generator, and not a simple cost calculator — it's a structured planning workspace built around specialized AI agents that each own one part of the plan, coordinated by an orchestrator and reviewed by a critic agent before being returned to the user.

## How it works

```
User fills the 8-step planner
        ↓
   Renovation Brief
        ↓
   AI Orchestrator
   ├─ Design Concept Agent
   ├─ Space Planning Agent
   ├─ Material Intelligence Agent
   ├─ Budget Agent
   ├─ Shopping List Agent
   ├─ Timeline Agent
   ├─ Execution Planner Agent
   └─ Critic Agent (validates, triggers targeted revisions)
        ↓
   Final Renovation Plan
```

The plan can then be adapted ("make it cheaper", "finish faster", "more sustainable", ...) or explored with "What if?" scenarios, saved locally, printed, downloaded as a PDF, or shared.

## Tech stack

- **Backend:** Python, FastAPI, Uvicorn, Pydantic, Jinja2
- **AI:** OpenAI Python SDK, `gpt-4.1-mini`, structured (Pydantic-validated) JSON outputs with retry + fallback
- **Frontend:** HTML, Tailwind CSS, vanilla JavaScript — no frontend framework, no build step
- **Storage:** JSON files for reference data (materials, inspiration, room types, design styles); `localStorage` for saved projects (no login, no database)

## Getting started

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

copy .env.example .env          # then fill in OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000**.

## Project structure

```
app/
├── main.py                 FastAPI app, static/template mounting, 404 handler
├── routes/                 pages.py, ai.py, materials.py, projects.py, feedback.py
├── agents/                 orchestrator.py + one agent per planning concern
├── services/                openai_service.py, json_store.py, pdf_service.py
├── models/                  Pydantic request/response models
├── data/                    materials.json, inspiration.json, room_types.json, design_styles.json
└── utils/                   validation.py, scoring.py, helpers.py

templates/                   Jinja2 pages (base.html + one per route)
static/
├── css/styles.css           design system (colors, type, components, print styles)
└── js/                      main.js, planner.js, plan.js, projects.js, materials.js, inspiration.js
```

## AI agents

| Agent | Responsibility |
|---|---|
| `design_agent` | Overall design concept: style, palette, materials/furniture/lighting/decor direction |
| `space_planning_agent` | Functional zones, furniture strategy, storage, movement flow — room-type aware |
| `material_agent` | Material recommendations and side-by-side comparisons with trade-offs |
| `budget_agent` | Budget allocation across categories, contingency, savings opportunities, scenario comparisons |
| `shopping_agent` | Prioritized, categorized shopping list with quantities and alternatives |
| `timeline_agent` | Phased schedule with dependencies and a critical path |
| `execution_agent` | Actionable tasks grouped by stage, flagged where a professional is recommended |
| `critic_agent` | Reviews the assembled plan for conflicts/gaps; orchestrator runs a targeted revision if needed |
| `orchestrator` | Runs the above concurrently where possible, assembles and validates the final plan |

## Important boundaries

This platform produces **planning estimates**, not contractor quotations, architectural drawings, or engineering approvals. For electrical, gas, structural, major plumbing, or roofing work, the plans explicitly recommend consulting a qualified professional rather than offering step-by-step DIY instructions.

## License

MIT — see [LICENSE](LICENSE).
