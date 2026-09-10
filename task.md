# CLAUDE CODE MASTER PROMPT

# Build a Complete AI Home Renovation Planning Platform

You are a **senior full-stack engineer, AI agent architect, product architect, UI/UX designer, and Python backend engineer**.

Build a **complete, polished, production-quality AI home renovation planning web application** called:

# **AI Home Renovation Planner**

This is NOT a basic interior-design form.

This is NOT a simple AI image generator.

This is NOT a generic chatbot.

This is NOT a simple room-cost calculator.

Build a sophisticated AI-powered renovation planning platform where specialized AI agents transform a user's room description, goals, budget, preferences, and constraints into a structured renovation concept, budget, shopping list, timeline, material alternatives, and execution plan.

The product should feel like a real premium home-design technology platform that could eventually be publicly launched.

---

# 1. CORE CONCEPT

The platform helps users answer:

> **"How should I renovate this room, how much will it cost, what do I need, and how do I execute it?"**

The primary workflow is:

```text
User
 ↓
Select Room
 ↓
Describe Current Space
 ↓
Define Renovation Goals
 ↓
Select Design Style
 ↓
Set Budget
 ↓
Set Room Dimensions
 ↓
Select Materials / Preferences
 ↓
Set Timeline
 ↓
AI Renovation Orchestrator
 ↓
Design Concept Agent
 ↓
Space Planning Agent
 ↓
Budget Agent
 ↓
Materials Agent
 ↓
Shopping List Agent
 ↓
Timeline Agent
 ↓
Execution Planner Agent
 ↓
AI Critic / Validation
 ↓
Final Renovation Plan
```

The user should never feel like they are simply chatting with AI.

The product should feel like an intelligent **renovation planning workspace**.

---

# 2. REQUIRED TECHNOLOGY

Use exactly:

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* OpenAI Python SDK
* Jinja2

## Frontend

* HTML
* Tailwind CSS
* Vanilla JavaScript

## AI Model

Use:

```text
OpenAI GPT-4.1-mini
```

Do not replace this with another model.

The OpenAI API key must remain server-side.

Do NOT use:

* React
* Next.js
* Vue
* Angular
* Node.js frontend
* separate frontend server
* PostgreSQL
* MongoDB
* Redis
* unnecessary microservices
* unnecessary infrastructure

FastAPI must serve the complete website.

Run with:

```bash
uvicorn app.main:app --reload --port 8000
```

Website:

```text
http://localhost:8000
```

---

# 3. IMPORTANT EXISTING STYLES FILE

Before changing the UI:

1. Inspect the existing styles file.
2. Understand its variables, utilities, components, spacing, typography, and design system.
3. Reuse compatible styles where appropriate.
4. Do not blindly delete useful existing styles.
5. Refactor only when necessary.
6. Keep styling maintainable.

If the existing styles file is empty or insufficient, create a complete professional styling system.

---

# 4. PRODUCT POSITIONING

The platform should combine:

```text
AI Interior Design Assistant
+
Renovation Cost Planner
+
Material Intelligence
+
Shopping Planner
+
Project Management
+
Execution Assistant
```

The system should answer questions such as:

```text
How can I renovate my bedroom for $3,000?

What materials should I use?

What should I buy first?

How long will the renovation take?

Where can I reduce costs?

What can I replace with a cheaper alternative?

What should be done before painting?

What is the correct order of renovation tasks?

How can I create a modern look without replacing everything?
```

---

# 5. DESIGN DIRECTION

Create a premium, sophisticated home-design experience.

Design language:

* premium
* editorial
* architectural
* modern
* warm
* minimal
* elegant
* light
* highly visual

The interface should feel like:

```text
Interior design magazine
+
Modern AI product
+
Renovation planning software
+
Premium home inspiration platform
```

Do NOT create:

* generic AI dashboard
* dark developer dashboard
* excessive gradients
* excessive glassmorphism
* generic SaaS cards
* cluttered forms
* template-looking UI

The product should feel intentionally designed for **home renovation**.

---

# 6. COLOR SYSTEM

Use a sophisticated light palette.

Base:

* warm white
* ivory
* cream
* soft beige
* stone
* neutral gray

Accent:

* muted olive
* warm terracotta
* natural brown
* subtle charcoal
* muted brass

Use color carefully.

Avoid neon colors.

Avoid excessive color usage.

---

# 7. TYPOGRAPHY

Use an editorial typography system.

Headings should feel:

* architectural
* premium
* expressive

Body text should remain:

* highly readable
* clean
* comfortable
* professional

Use strong visual hierarchy.

Do not make everything bold.

---

# 8. RESPONSIVE DESIGN

The application must be fully responsive.

Support:

```text
Large Desktop
Desktop
Laptop
Tablet
Mobile
```

Do not simply shrink desktop layouts.

Create intentional mobile experiences.

The renovation planner must remain easy to use on phones.

---

# 9. GLOBAL NAVBAR

Create a polished navbar.

Desktop:

```text
Logo
Home
Plan Renovation
Projects
Inspiration
Materials
Saved

Search

[Start Planning]
```

Mobile:

```text
Logo
Menu
```

Mobile navigation must contain all important links.

Navbar should have subtle border/shadow behavior on scroll.

---

# 10. HOME PAGE

Create a complete homepage.

Sections:

```text
Navbar
Hero
AI Renovation Planner
Explore Room Types
Design Styles
Featured Renovation Concepts
How It Works
Budget Planning
Material Intelligence
Renovation Process
CTA
Footer
```

---

# 11. HERO SECTION

The hero should immediately explain the product.

Example:

```text
Plan the renovation.
Before you spend the money.

Turn your room, budget, and ideas
into a complete renovation plan with AI.

[Plan My Renovation]

[Explore Ideas]
```

Include an elegant architectural/home visual composition.

Do not depend on remote image URLs for core functionality.

If assets are unavailable, use polished local placeholders that do not look broken.

---

# 12. RENOVATION PLANNER

This is the primary product feature.

Create a highly polished guided planning experience.

CTA:

```text
Start Renovation Plan
```

Opening the planner should feel like entering an intelligent design studio.

Use a visual multi-step progress system:

```text
1 Space
2 Goals
3 Style
4 Budget
5 Materials
6 Timeline
7 Review
8 AI Plan
```

---

# 13. STEP 1: ROOM TYPE

Ask:

```text
What are you renovating?
```

Options:

```text
Living Room
Bedroom
Kitchen
Bathroom
Dining Room
Home Office
Entryway
Balcony
Outdoor Area
Nursery
Guest Room
Basement
Other
```

Use visual selection cards.

---

# 14. STEP 2: CURRENT SPACE

Ask:

```text
Tell us about your current space.
```

Fields:

```text
Room dimensions
Current condition
Existing furniture
Existing flooring
Existing walls
Existing lighting
Windows / doors
Major structural constraints
```

Allow room dimensions:

```text
Length
Width
Height
Unit
```

Support:

```text
Feet
Meters
```

Also allow:

```text
I don't know the exact dimensions
```

Do not prevent users from continuing when measurements are unavailable.

---

# 15. STEP 3: RENOVATION GOALS

Ask:

```text
What do you want to achieve?
```

Options:

```text
Modernize
Make the room brighter
Increase storage
Improve functionality
Make it feel larger
Create a luxury look
Reduce maintenance
Improve lighting
Improve organization
Increase comfort
Prepare for resale
Complete makeover
Partial renovation
```

Allow multiple selections.

Also provide:

```text
Describe your goal...
```

---

# 16. STEP 4: DESIGN STYLE

Provide:

```text
Modern
Minimalist
Scandinavian
Industrial
Japandi
Traditional
Contemporary
Luxury
Bohemian
Mid-Century Modern
Rustic
Coastal
Classic
Eclectic
Custom
```

Allow a custom description.

Example:

```text
Warm modern style with neutral colors,
wood accents, and minimal furniture.
```

---

# 17. STEP 5: COLOR PREFERENCES

Allow users to select:

```text
Warm neutrals
Cool neutrals
Earth tones
White & beige
Black & white
Green
Blue
Terracotta
Natural wood
Custom
```

Allow:

```text
Colors I want
Colors I don't want
```

The AI should respect these preferences.

---

# 18. STEP 6: BUDGET

Ask:

```text
What's your renovation budget?
```

Presets:

```text
Low
Moderate
Premium
Luxury
```

Also support:

```text
Custom
```

Fields:

```text
Currency
Maximum Budget
```

Example:

```text
PKR 500,000
USD 5,000
EUR 4,000
```

The generated plan must respect the selected budget.

Do not pretend estimated costs are live market prices.

Clearly label them as:

```text
Estimated Planning Cost
```

---

# 19. BUDGET ALLOCATION

The AI should divide the estimated budget across:

```text
Materials
Furniture
Lighting
Labor
Decor
Storage
Contingency
```

Example:

```text
Estimated Budget
PKR 500,000

Materials       35%
Furniture       25%
Labor           20%
Lighting        10%
Decor            5%
Contingency      5%
```

The allocation must add up correctly.

---

# 20. STEP 7: MATERIAL PREFERENCES

Allow users to specify:

```text
Flooring
Wall finish
Paint
Countertops
Cabinet materials
Hardware
Lighting
Furniture materials
```

Preference options:

```text
Natural
Budget-friendly
Premium
Low-maintenance
Durable
Eco-conscious
Easy to clean
Custom
```

The system should recommend materials based on room type, budget, style, and use case.

---

# 21. MATERIAL INTELLIGENCE AGENT

Create:

```text
app/agents/material_agent.py
```

Responsibilities:

* recommend appropriate materials
* compare material alternatives
* consider durability
* consider maintenance
* consider budget
* consider style compatibility
* explain trade-offs

Example:

```text
Material:
Engineered Wood Flooring

Why:
Lower maintenance than solid hardwood
and more budget-friendly.

Alternative:
Luxury Vinyl

Trade-off:
Lower cost and strong moisture resistance,
but different visual/texture characteristics.
```

Do not make unsupported technical or safety claims.

---

# 22. SPACE PLANNING AGENT

Create:

```text
app/agents/space_planning_agent.py
```

Responsibilities:

* understand room dimensions
* determine functional zones
* recommend furniture placement concepts
* identify storage opportunities
* improve movement flow
* consider doors and windows
* respect known constraints

Example:

```text
Zone 1:
Conversation Area

Zone 2:
Media Wall

Zone 3:
Storage

Recommended Flow:
Maintain clear circulation between entrance
and main seating area.
```

Do not claim exact architectural compliance.

Clearly label suggestions as planning concepts.

---

# 23. DESIGN CONCEPT AGENT

Create:

```text
app/agents/design_agent.py
```

Responsibilities:

* create overall design concept
* combine style
* colors
* materials
* furniture
* lighting
* decor
* functionality

Output:

```json
{
  "concept_name": "",
  "design_summary": "",
  "style": "",
  "color_palette": [],
  "materials": [],
  "furniture_direction": [],
  "lighting_direction": [],
  "decor_direction": [],
  "design_priorities": []
}
```

---

# 24. BUDGET AGENT

Create:

```text
app/agents/budget_agent.py
```

Responsibilities:

* estimate planning costs
* allocate budget
* identify expensive areas
* identify savings opportunities
* create contingency
* compare budget scenarios

Output:

```json
{
  "currency": "",
  "total_estimate": 0,
  "categories": [],
  "contingency": 0,
  "savings_opportunities": [],
  "budget_risk": "",
  "assumptions": []
}
```

Do not represent estimates as quotations.

---

# 25. SHOPPING LIST AGENT

Create:

```text
app/agents/shopping_agent.py
```

Responsibilities:

* convert renovation plan into purchase requirements
* group items by category
* prioritize purchases
* estimate quantities
* identify optional items
* identify alternatives

Categories:

```text
Paint
Flooring
Lighting
Furniture
Hardware
Storage
Decor
Tools
Materials
```

Each item:

```json
{
  "name": "",
  "category": "",
  "quantity": "",
  "estimated_cost": 0,
  "priority": "",
  "alternative": "",
  "notes": ""
}
```

---

# 26. TIMELINE AGENT

Create:

```text
app/agents/timeline_agent.py
```

Responsibilities:

* sequence renovation tasks
* identify dependencies
* estimate task durations
* create phases
* identify critical path
* identify tasks that can run in parallel

Example:

```text
PHASE 1
Preparation
2 days

PHASE 2
Electrical / Lighting
3 days

PHASE 3
Painting
2 days

PHASE 4
Flooring
3 days

PHASE 5
Furniture & Styling
2 days
```

Do not provide guarantees about contractor timelines.

Clearly label durations as estimates.

---

# 27. EXECUTION PLANNER AGENT

Create:

```text
app/agents/execution_agent.py
```

Responsibilities:

* convert the design into actionable tasks
* establish task dependencies
* identify required tools/materials
* identify tasks requiring qualified professionals
* create preparation checklist
* create final inspection checklist

Example:

```text
Task:
Prepare walls

Dependencies:
Remove wall fixtures

Materials:
Primer
Filler
Sandpaper

Recommended Skill:
Professional recommended for major wall repair
```

Do not provide unsafe DIY instructions for structural, electrical, gas, plumbing, or other high-risk work.

---

# 28. RENOVATION CRITIC AGENT

Create:

```text
app/agents/critic_agent.py
```

The critic reviews the generated plan for:

```text
Budget conflicts
Timeline conflicts
Material mismatches
Style inconsistencies
Missing tasks
Missing dependencies
Unrealistic quantities
User preference violations
```

The critic should return:

```json
{
  "issues": [],
  "warnings": [],
  "improvements": [],
  "approved": true
}
```

If issues are found, the orchestrator should revise the relevant output.

---

# 29. AI ORCHESTRATOR

Create:

```text
app/agents/orchestrator.py
```

Coordinate the complete workflow:

```text
User Preferences
      ↓
Preference Validation
      ↓
Design Concept Agent
      ↓
Space Planning Agent
      ↓
Material Agent
      ↓
Budget Agent
      ↓
Shopping Agent
      ↓
Timeline Agent
      ↓
Execution Agent
      ↓
Critic Agent
      ↓
Revision if Necessary
      ↓
Final Renovation Plan
```

Do not run every agent unnecessarily.

Use the minimum agents required for each workflow.

---

# 30. STRUCTURED AI OUTPUT

Every agent must return structured JSON.

Use Pydantic models to validate every AI response.

Do not depend on free-form text parsing.

If invalid output occurs:

```text
Validate
 ↓
Retry safely
 ↓
Fallback
```

Never expose raw model responses.

---

# 31. FINAL RENOVATION PLAN

After generation, create a beautiful planning workspace.

Top section:

```text
YOUR RENOVATION PLAN

Warm Modern Living Room

Estimated Budget:
PKR 485,000

Estimated Timeline:
12–15 days

Style:
Warm Modern

Planning Confidence:
High
```

Then sections:

```text
Design Concept
Space Plan
Budget
Materials
Shopping List
Timeline
Execution Plan
Alternatives
AI Recommendations
Assumptions
Warnings
```

---

# 32. DESIGN CONCEPT PAGE

Show:

```text
Concept Name
Design Summary
Style
Color Palette
Material Direction
Furniture Direction
Lighting Direction
Decor Direction
```

Include visual color swatches.

Use elegant design cards.

---

# 33. SPACE PLAN

Display:

```text
Room Dimensions
Functional Zones
Furniture Strategy
Storage Strategy
Movement Flow
Lighting Zones
```

If exact dimensions are missing:

```text
Planning based on user-provided approximate information.
```

Never pretend to have created a construction-grade floor plan.

---

# 34. BUDGET DASHBOARD

Create a visually strong budget section.

Example:

```text
TOTAL ESTIMATE

PKR 485,000

Materials       PKR 170,000
Furniture       PKR 120,000
Labor           PKR 95,000
Lighting        PKR 45,000
Decor           PKR 30,000
Contingency     PKR 25,000
```

Include:

```text
Budget Used
Remaining
Potential Savings
Risk Level
```

Use CSS/JavaScript visualizations where useful.

Do not use heavy chart libraries unnecessarily.

---

# 35. BUDGET SCENARIOS

Allow users to compare:

```text
Budget Version
Balanced Version
Premium Version
```

Example:

```text
BUDGET

Estimated:
PKR 320,000

BALANCED

Estimated:
PKR 485,000

PREMIUM

Estimated:
PKR 720,000
```

Each scenario should explain what changes.

---

# 36. MATERIAL COMPARISON

Allow users to compare alternatives.

Example:

```text
Flooring

Option A
Engineered Wood

Cost:
Medium

Maintenance:
Medium

Style Fit:
Excellent

Option B
Luxury Vinyl

Cost:
Low

Maintenance:
Low

Style Fit:
Good
```

Add:

```text
AI Recommendation
```

Explain trade-offs rather than declaring one material universally best.

---

# 37. SHOPPING LIST

Create an interactive shopping list.

Example:

```text
☐ 10L Warm White Paint
☐ 25m² Flooring
☐ 2 Pendant Lights
☐ 1 Area Rug
☐ 4 Dining Chairs
☐ Wall Shelving
```

Features:

```text
Check item
Uncheck item
Filter by category
Show optional items
Show priority items
```

Store checklist state locally.

---

# 38. SHOPPING PRIORITIES

Every item should have:

```text
Essential
Recommended
Optional
```

Allow filtering.

---

# 39. RENOVATION TIMELINE

Create a visual timeline.

Example:

```text
DAY 1–2
Preparation

DAY 3–5
Electrical + Lighting

DAY 6–7
Painting

DAY 8–10
Flooring

DAY 11–12
Furniture

DAY 13–14
Styling + Final Inspection
```

Show dependencies.

Allow users to mark tasks:

```text
Not Started
In Progress
Completed
```

Store progress locally.

---

# 40. EXECUTION CHECKLIST

Create:

```text
Before Renovation
During Renovation
Installation
Styling
Final Inspection
```

Example:

```text
Before Renovation

☐ Confirm measurements
☐ Finalize materials
☐ Confirm furniture dimensions
☐ Protect existing areas
☐ Schedule required professionals
```

---

# 41. AI ADAPTATION

Add:

```text
Adapt My Plan
```

Options:

```text
Make it cheaper
Make it more luxurious
Finish faster
Use more sustainable materials
Make it minimalist
Add more storage
Keep existing furniture
Reduce construction work
Change color palette
```

The AI must preserve the overall structure while modifying the relevant parts.

---

# 42. AI "WHAT IF?" MODE

This should be a standout feature.

Allow users to ask:

```text
What if I reduce the budget by 20%?

What if I keep my existing sofa?

What if I finish the renovation in 7 days?

What if I replace hardwood with a cheaper material?

What if I prioritize storage instead of decor?
```

The system should calculate the impact on:

```text
Budget
Timeline
Materials
Design
Functionality
```

Then show:

```text
CHANGE IMPACT

Budget:
-20%

Timeline:
No significant change

Design:
Moderate impact

Recommendation:
Keep the lighting investment and downgrade
decor items first.
```

---

# 43. ROOM-SPECIFIC INTELLIGENCE

Adapt recommendations according to room type.

For example:

### Kitchen

Consider:

```text
Cabinetry
Countertops
Storage
Lighting
Appliances
Workflow
```

### Bedroom

Consider:

```text
Bed placement
Storage
Lighting
Comfort
Color
Privacy
```

### Bathroom

Consider:

```text
Fixtures
Storage
Lighting
Surfaces
Maintenance
```

### Living Room

Consider:

```text
Seating
Entertainment
Lighting
Circulation
Storage
Decor
```

Do not apply the exact same planning logic to every room.

---

# 44. EXISTING FURNITURE

Allow users to list furniture they want to keep.

Example:

```text
Keep:

Sofa
Dining table
TV
Bookshelf
Bed
```

The AI should incorporate these into the plan where appropriate.

Also allow:

```text
Replace
Keep
Unsure
```

---

# 45. BEFORE / AFTER CONCEPT

Create a visual planning section:

```text
CURRENT SPACE

Description
Existing Issues

↓

RENOVATION DIRECTION

Design Concept

↓

TARGET SPACE

Expected Result
```

Do not generate fake photorealistic before/after images.

Represent the transformation as a design concept unless an actual image-generation integration is explicitly implemented.

---

# 46. SAVED PROJECTS

Since there is no authentication, use localStorage.

Users can:

```text
Save Project
Rename Project
Delete Project
Open Project
```

Create:

```text
/projects
```

Show:

```text
My Renovation Projects
```

Empty state:

```text
You haven't planned a renovation yet.

Start your first renovation plan.

[Start Planning]
```

---

# 47. PROJECT DASHBOARD

Each saved project should show:

```text
Project Name
Room
Style
Budget
Timeline
Progress
Last Updated
```

Example:

```text
Warm Modern Bedroom

Budget:
PKR 350,000

Timeline:
10 days

Progress:
45%
```

---

# 48. SEARCH AND INSPIRATION

Create:

```text
/inspiration
```

Provide inspiration categories:

```text
Living Rooms
Bedrooms
Kitchens
Bathrooms
Minimalist
Modern
Luxury
Small Spaces
Budget Renovations
```

Use local sample content.

Do not depend on external image URLs for core functionality.

---

# 49. SEARCH

Implement search across:

```text
Projects
Inspiration
Materials
Room Types
Design Styles
```

Support queries such as:

```text
modern bedroom
small kitchen
budget renovation
warm minimalist
storage ideas
```

---

# 50. MATERIAL LIBRARY

Create:

```text
/materials
```

Show a structured library of:

```text
Flooring
Paint
Wall Finishes
Lighting
Countertops
Cabinet Materials
Hardware
Furniture Materials
```

Each material:

```text
Name
Category
Style Compatibility
Cost Level
Maintenance
Durability
Common Uses
Alternatives
```

Clearly label this as planning/reference data.

Do not present fictional supplier prices as live market prices.

---

# 51. MATERIAL DETAIL PAGE

Create:

```text
/material/{slug}
```

Show:

```text
Material Name
Description
Typical Cost Level
Maintenance
Style Compatibility
Best Uses
Alternatives
AI Notes
```

---

# 52. ABOUT PAGE

Create:

```text
/about
```

Explain:

```text
What the platform does
How AI renovation planning works
How budget planning works
How material alternatives work
How the execution plan is created
```

Keep it professional.

---

# 53. FAQ PAGE

Create:

```text
/faq
```

Questions:

```text
How does the AI create renovation plans?
Are budget estimates exact?
Can I keep existing furniture?
Can I change the design style?
Can I compare materials?
Can I adjust the budget?
Can I save renovation projects?
Does this replace an architect or contractor?
```

---

# 54. CONTACT PAGE

Create:

```text
/contact
```

Fields:

```text
Name
Email
Subject
Message
```

Store submissions locally.

Do not pretend messages are actually emailed.

Show:

```text
Message received.
```

---

# 55. FOOTER

Create:

```text
AI Home Renovation Planner

Plan smarter.
Renovate with confidence.

Explore
Inspiration
Materials
Projects
Plan Renovation

AI Tools
Renovation Planner
Budget Planner
Material Intelligence
What-If Mode

Company
About
FAQ
Contact

© 2026 AI Home Renovation Planner
```

---

# 56. API DESIGN

Implement clean FastAPI routes.

Example:

```text
GET  /
GET  /planner
GET  /projects
GET  /inspiration
GET  /materials
GET  /material/{slug}
GET  /about
GET  /faq
GET  /contact

GET  /api/materials
GET  /api/materials/{id}
GET  /api/inspiration
GET  /api/search

POST /api/ai/create-plan
POST /api/ai/adapt-plan
POST /api/ai/what-if
POST /api/ai/material-alternatives
POST /api/ai/space-plan
POST /api/ai/budget
POST /api/feedback

POST /api/contact
```

Use proper Pydantic request and response models.

---

# 57. OPENAI SERVICE

Create:

```text
app/services/openai_service.py
```

Centralize OpenAI communication.

Functions:

```python
generate_design_concept()
generate_space_plan()
generate_material_plan()
generate_budget()
generate_shopping_list()
generate_timeline()
generate_execution_plan()
critique_renovation_plan()
adapt_renovation_plan()
run_what_if_scenario()
```

Do not scatter OpenAI API calls throughout route files.

---

# 58. AGENT ARCHITECTURE

Maintain clean separation:

```text
User Request
     ↓
Preference Extraction
     ↓
Renovation Orchestrator
     ↓
Specialized Agents
     ↓
Validation
     ↓
Critic
     ↓
Revision
     ↓
Final Renovation Plan
```

Do not send unnecessary data to OpenAI.

Pass only the relevant project context to each agent.

---

# 59. DATA STORAGE

Use JSON files for persistent application data.

Example:

```text
app/data/
├── materials.json
├── inspiration.json
├── room_types.json
├── design_styles.json
├── feedback.json
└── contacts.json
```

Create reusable JSON storage utilities.

Do not duplicate read/write logic.

---

# 60. PROJECT STRUCTURE

Use:

```text
ai-home-renovation-planner/
│
├── app/
│   ├── main.py
│
│   ├── routes/
│   │   ├── pages.py
│   │   ├── projects.py
│   │   ├── materials.py
│   │   ├── ai.py
│   │   └── feedback.py
│
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── design_agent.py
│   │   ├── space_planning_agent.py
│   │   ├── material_agent.py
│   │   ├── budget_agent.py
│   │   ├── shopping_agent.py
│   │   ├── timeline_agent.py
│   │   ├── execution_agent.py
│   │   └── critic_agent.py
│
│   ├── services/
│   │   ├── openai_service.py
│   │   ├── renovation_service.py
│   │   └── json_store.py
│
│   ├── models/
│   │   ├── renovation.py
│   │   ├── material.py
│   │   ├── project.py
│   │   ├── ai_request.py
│   │   └── feedback.py
│
│   ├── data/
│   │   ├── materials.json
│   │   ├── inspiration.json
│   │   ├── room_types.json
│   │   ├── design_styles.json
│   │   ├── feedback.json
│   │   └── contacts.json
│
│   └── utils/
│       ├── validation.py
│       ├── scoring.py
│       └── helpers.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── planner.html
│   ├── plan.html
│   ├── projects.html
│   ├── project.html
│   ├── inspiration.html
│   ├── materials.html
│   ├── material.html
│   ├── about.html
│   ├── contact.html
│   ├── faq.html
│   └── 404.html
│
├── static/
│   ├── css/
│   │   └── styles.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── planner.js
│   │   ├── plan.js
│   │   ├── projects.js
│   │   ├── materials.js
│   │   └── inspiration.js
│   │
│   └── images/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

Adapt this structure if the existing project already has a better structure.

Maintain clean separation of responsibilities.

---

# 61. ENVIRONMENT

Create:

```text
.env.example
```

with:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

Never hardcode API keys.

---

# 62. AI COST CONTROL

Do not call AI unnecessarily.

Use:

```text
User Input
 ↓
Local Validation
 ↓
Relevant Context
 ↓
Specialized Agent
```

Avoid sending large datasets or irrelevant project information to OpenAI.

---

# 63. PERFORMANCE

Optimize the application.

Important:

* avoid unnecessary AI requests
* minimize JavaScript
* lazy-load images
* keep API payloads clean
* use local filtering where possible
* cache suitable calculations
* use asynchronous FastAPI operations where appropriate
* avoid blocking the UI

---

# 64. LOADING EXPERIENCE

Every AI operation requires a polished contextual loading state.

Example:

```text
Creating Your Renovation Plan

✓ Understanding your room
✓ Reviewing your goals
✓ Building the design concept
● Planning materials
○ Estimating budget
○ Creating shopping list
○ Building timeline
○ Reviewing the final plan
```

Do not use a generic spinner everywhere.

---

# 65. TOAST SYSTEM

Create a reusable toast system.

Examples:

```text
Project saved
Project deleted
Plan updated
Shopping item completed
Task completed
Plan adapted
Scenario calculated
Link copied
Feedback submitted
```

---

# 66. EMPTY STATES

Create polished empty states.

Never show a blank page.

Example:

```text
No renovation projects yet.

Turn your next room idea
into a complete renovation plan.

[Start Planning]
```

---

# 67. 404 PAGE

Create a polished 404 page.

Example:

```text
Looks like this room
doesn't exist yet.

[Back Home]
[Start Planning]
```

---

# 68. SHARE AND EXPORT

Allow users to:

```text
Share Renovation Plan
Copy Link
Print Plan
Download Plan
```

Use Web Share API where available.

Fallback:

```text
Copy Link
```

Implement a polished print layout.

For downloadable output, generate a clean PDF containing:

```text
Project Overview
Design Concept
Budget
Materials
Shopping List
Timeline
Execution Plan
Warnings
Assumptions
```

Do not generate a broken plain-text PDF.

---

# 69. PRINT MODE

When printing:

Hide:

* navbar
* interactive controls
* unnecessary navigation
* editing buttons

Show only:

```text
Project Overview
Design
Budget
Materials
Shopping List
Timeline
Execution Plan
```

---

# 70. SAFETY AND PROFESSIONAL BOUNDARIES

The platform is a planning assistant.

Do NOT claim that AI plans are:

```text
architectural drawings
engineering plans
construction approvals
professional inspections
guaranteed cost estimates
guaranteed timelines
```

For high-risk work involving:

```text
Electrical
Gas
Structural changes
Major plumbing
Load-bearing walls
Roofing
```

clearly recommend consulting qualified professionals.

Do not provide dangerous step-by-step instructions for high-risk construction work.

---

# 71. COST ESTIMATION DISCLAIMER

Every generated budget should clearly state:

```text
These are planning estimates, not contractor quotations.
Actual costs vary by location, labor, materials, availability,
and project conditions.
```

Do not present fabricated prices as current market prices.

---

# 72. WHAT-IF VALIDATION

Every scenario change must validate:

```text
Budget
Timeline
Materials
Dependencies
User Goals
```

Example:

```text
If budget decreases by 20%:

Remove:
Premium decorative lighting

Keep:
Core electrical work

Change:
Flooring option

Impact:
Lower aesthetic flexibility
No major timeline change
```

---

# 73. FINAL REVIEW SCREEN

Before AI generation, show:

```text
YOUR RENOVATION BRIEF

Room:
Living Room

Dimensions:
15 × 12 ft

Goal:
Modernize + Improve Storage

Style:
Warm Modern

Budget:
PKR 500,000

Colors:
Beige + Natural Wood

Keep:
Existing Sofa

Timeline:
14 Days
```

Allow editing every section.

Button:

```text
Generate My Renovation Plan
```

---

# 74. FINAL AI PLAN EXPERIENCE

After generation:

```text
Your renovation plan is ready.

Warm Modern Living Room

Budget:
PKR 485,000

Timeline:
12–15 days

Design Match:
High

Budget Risk:
Low

[View Full Plan]
[Save Project]
[Download PDF]
[Adapt Plan]
```

The transition should feel polished.

---

# 75. IMPORTANT: DO NOT BUILD A FAKE UI

Every major interaction must work.

These must actually work:

```text
Planner
Room selection
Dimension input
Goal selection
Style selection
Budget calculation
Material recommendations
AI generation
Budget scenarios
Material comparison
Shopping list
Timeline
Execution checklist
What-If mode
Plan adaptation
Save project
Delete project
Search
Filtering
Print
Download
Share
Navigation
```

Do not create buttons that only visually respond.

---

# 76. FINAL TESTING

Test the complete journey:

```text
Home
 ↓
Start Planning
 ↓
Select Bedroom
 ↓
Enter Dimensions
 ↓
Select Renovation Goals
 ↓
Select Modern Style
 ↓
Set Budget
 ↓
Select Materials
 ↓
Review
 ↓
Generate AI Plan
 ↓
Design Concept
 ↓
Space Plan
 ↓
Budget
 ↓
Materials
 ↓
Shopping List
 ↓
Timeline
 ↓
Execution Plan
 ↓
What-If Scenario
 ↓
Adapt Plan
 ↓
Save Project
 ↓
Download
 ↓
Print
 ↓
Share
```

Test on:

```text
Desktop
Tablet
Mobile
```

Fix all broken states.

---

# 77. FINAL QUALITY BAR

The final application must NOT look like:

```text
student project
basic CRUD application
AI chatbot
generic calculator
generic dashboard
generic Tailwind template
prototype
```

It should look like:

```text
A premium AI-powered renovation planning product.
```

Pay special attention to:

* visual hierarchy
* architecture-inspired UI
* room imagery
* typography
* spacing
* budget visualization
* material comparison
* planner UX
* progress states
* mobile experience
* shopping checklist
* timeline visualization
* empty states
* loading states
* accessibility
* responsive behavior

---

# 78. FINAL IMPLEMENTATION REQUIREMENT

Do not stop after creating the initial pages.

Continue implementing until the complete application works end-to-end.

Inspect the existing project before modifying it.

Reuse the existing styles file where appropriate.

Do not ask me to design the UI for you.

You are responsible for all UI/UX decisions.

Use:

```text
Python
FastAPI
Uvicorn
Pydantic
OpenAI Python SDK
Jinja2
HTML
Tailwind CSS
Vanilla JavaScript
GPT-4.1-mini
```

No login or signup.

No unnecessary infrastructure.

No fake live market pricing.

No fake contractor quotations.

No fake architectural certification.

No unsupported safety claims.

The final product should be a **complete AI-powered home renovation intelligence and planning platform**, where specialized AI agents collaborate to transform a user's renovation goals into a structured, actionable plan.

Build it to a level where the interface should require **little to no manual UI redesign after implementation**.
