# Autonomous AI Persona Backend (Python)

Production-quality autonomous AI content creator backend built with **Python 3.12+**, **FastAPI**, **SQLAlchemy 2.0 (Async)**, **PostgreSQL**, **Alembic**, **APScheduler**, and **Pydantic v2**.

The system operates autonomously without human prompts after initialization, generating technical persona-aligned posts on a background schedule and serving them via a read-only feed API.

---

## System Architecture & Features

```
Discover Topics (HN, GitHub, arXiv, RSS)
                 │
                 ▼
       Editorial Filtering
     (Scoring & Rule Checking)
                 │
                 ▼
          Memory Engine
 (DB Deduplication & Similarity Check)
                 │
                 ▼
          Prompt Builder
      (Persona + Style Rules)
                 │
                 ▼
           LLM Provider
     (OpenAI / Interchangeable)
                 │
                 ▼
            Store Post
         (PostgreSQL DB)
```

1. **Autonomous Background Scheduler (**`APScheduler`**)**:
  - Runs the discovery-editorial-memory-publishing pipeline automatically every 30 minutes (configurable).
  - Starts upon agent initialization (`POST /api/agent/init`) or system startup.
2. **Topic Discovery Services**:
  - Abstract `TopicProvider` interface (`async def fetch_topics(self)`).
  - Implementations: Hacker News API, GitHub Trending / Search, arXiv API, RSS Feeds (OpenAI, Anthropic, DeepMind, TechCrunch).
3. **Editorial Engine**:
  - Scores topics across 6 dimensions: Importance, Novelty, Credibility, Persona Fit, Recency, and Duplicate Penalty.
  - Rejects clickbait, promotional content, old news, and low-relevance topics.
  - Stores rejected topics in PostgreSQL with detailed rejection reasons.
4. **Persona Engine**:
  - Dynamic persona profiling for any domain (with built-in optimized default for **AI Security**).
  - Defines domain keywords (e.g. Prompt Injection, Red Teaming, CVEs), tone, vocabulary, and strict style rules (e.g. No emojis, No hype, Evidence-driven).
5. **Memory System**:
  - Persists published posts, covered topics, and rejected topics in PostgreSQL.
  - Performs text similarity checks (Jaccard + Sequence matcher) against existing history before publishing to prevent duplicates.
6. **Prompt Builder & LLM Abstraction**:
  - Constructs structured, context-aware prompts.
  - `LLMProvider` abstraction supporting OpenAI API and high-quality Mock provider for testing and offline fallback environments.
7. **Strict API Contracts**:
  - `POST /api/agent/init`: Initializes agent and starts autonomous cycle.
  - `GET /api/agent/feed?agentId=<uuid>`: Reads persisted posts sorted **Newest First**. *Never triggers content generation on GET.*

---



## API Endpoints



### 1. Initialize Agent

- **Endpoint**: `POST /api/agent/init`
- **Request Body**:

```json
{
  "persona": {
    "name": "Ada",
    "domain": "AI Security"
  }
}
```

- **Response**:

```json
{
  "agentId": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```



### 2. Retrieve Agent Feed

- **Endpoint**: `GET /api/agent/feed?agentId=3fa85f64-5717-4562-b3fc-2c963f66afa6`
- **Response**:

```json
{
  "posts": [
    {
      "id": "c7a6f23b-5a1e-4b9d-8d4e-2f1a9b3c4d5e",
      "createdAt": "2026-08-08T02:00:00Z",
      "text": "Technical Analysis of Zero-Day Prompt Injection Attacks...",
      "rationale": "Selection Rationale: 1) Why selected... 2) Why relevant now... 3) Why chosen over alternatives...",
      "sources": [
        "https://arxiv.org/abs/2401.00001"
      ]
    }
  ]
}
```

---



## Quickstart & Local Setup



### Prerequisites

- Python 3.12+
- Docker & Docker Compose (optional for PostgreSQL container)



### Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```



### Run Tests

```bash
pytest -v
```



### Run Server Locally

```bash
uvicorn app.main:app --reload --port 8000
```

---



## Docker Setup

To run with PostgreSQL database in Docker:

```bash
docker-compose up --build
```

The application will automatically run Alembic database migrations and start the uvicorn web server at `http://localhost:8000`.

---



## Testing & Verification

Run the full pytest test suite:

```bash
pytest tests/
```

# Autonomous AI Creator — Frontend

A dashboard for **Autonomous AI Creator**, a system that autonomously discovers AI/technology topics, evaluates them editorially, generates content, and publishes it over time — without a human prompt for each post.

The frontend is the visual control and monitoring layer for this agent: its activity, editorial decisions, discovered topics, and generated publications.

---

## About the Project

Most AI content tools need a human prompt for every piece of content. Autonomous AI Creator instead runs a continuous loop:

1. Discover new AI/technology topics
2. Evaluate whether a topic is worth publishing
3. Reject irrelevant or low-value topics
4. Check against previously published content
5. Generate content using a consistent AI persona
6. Publish selected content
7. Repeat — without a new human prompt

---

## Features


| Section                    | What it shows                                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Agent Overview**         | Persona name, domain, status, and operating mode                                                           |
| **System Metrics**         | Sources monitored, topics discovered/rejected, publications generated                                      |
| **Live Scanning**          | Visual of the agent monitoring sources (Hacker News, GitHub, arXiv, RSS)                                   |
| **Activity Timeline**      | The pipeline in progress: Scan → Discover → Evaluate → Filter → Memory Check → Select → Generate → Publish |
| **Editorial Decisions**    | Why topics are rejected (irrelevant, low-value, repetitive, off-domain, etc.)                              |
| **Live Intelligence Feed** | Generated posts, each with content, timestamp, rationale, and sources                                      |
| **Post Cards**             | Reusable card UI for displaying each publication                                                           |


Together, these make the agent's reasoning visible rather than just showing a final post.

---

## Architecture

```
src/
├── components/
│   ├── ActivityTimeline.jsx
│   ├── AgentOverview.jsx
│   ├── EditorialPanel.jsx
│   ├── Feed.jsx
│   ├── Header.jsx
│   ├── LiveScanning.jsx
│   ├── MetricRow.jsx
│   ├── PostCard.jsx
│   ├── Sidebar.jsx
│   └── StatusBadge.jsx
├── services/
│   └── api.js        # Backend API communication
├── utils/
│   └── format.js      # Timestamp/data formatting helpers
├── App.jsx
├── App.css
└── index.css

```

## Tech Stack

React · Vite · JavaScript/JSX · CSS · ESLint

---

## Getting Started

**Prerequisites:** Node.js, npm, Git

```bash
# Clone
git clone https://github.com/abhinav-codes123/Autonomous-AI-Creator.git
cd Autonomous-AI-Creator

# Install
npm install

# Run
npm run dev   # → http://localhost:5173

```

**Other commands:**

```bash
npm run lint      # Run linter
npm run build     # Production build
npm run preview   # Preview production build

```

---

## Backend Integration

The frontend expects two endpoints, called from `src/services/api.js`:

**Initialize agent**

```
POST /api/agent/init

```

```json
// Request
{ "persona": { "name": "Ada", "domain": "AI Security" } }

// Response
{ "agentId": "abc-123" }

```

**Retrieve feed**

```
GET /api/agent/feed?agentId=abc-123

```

```json
{
  "posts": [
    {
      "id": "p7",
      "createdAt": "2026-08-07T10:30:00Z",
      "text": "Example publication...",
      "rationale": "Why this topic was selected and why it is relevant now.",
      "sources": ["https://example.com/source"]
    }
  ]
}

```

**Data flow:**

```
Init Agent → Backend returns Agent ID → GET /api/agent/feed → Live Intelligence Feed

```

The backend runs autonomously after initialization; the frontend just renders its output.

---

## UI Layout

```
┌─────────────────────────────────────────────────────┐
│                      HEADER                         │
├───────────────┬─────────────────────────────────────┤
│               │        AGENT OVERVIEW                │
│   SIDEBAR     ├─────────────────────────────────────┤
│               │        SYSTEM METRICS                │
│               ├─────────────────────────────────────┤
│               │        LIVE SCANNING                 │
│               ├───────────────────┬─────────────────┤
│               │ ACTIVITY TIMELINE │ EDITORIAL        │
│               │                   │ DECISIONS        │
│               ├───────────────────┴─────────────────┤
│               │      LIVE INTELLIGENCE FEED          │
└───────────────┴─────────────────────────────────────┘

```

---

## Project Files


| File / Folder                        | Purpose                     |
| ------------------------------------ | --------------------------- |
| `src/App.jsx`                        | Main application component  |
| `src/App.css`, `src/index.css`       | Styling                     |
| `src/components/`                    | Reusable UI components      |
| `src/services/api.js`                | Backend API communication   |
| `src/utils/format.js`                | Helper/formatting functions |
| `public/`                            | Static assets               |
| `index.html`                         | HTML entry point            |
| `package.json`                       | Dependencies and scripts    |
| `vite.config.js`, `eslint.config.js` | Build/lint config           |


---

## Status

**Done:** dashboard UI, agent overview, status indicators, system metrics, live scanning, activity timeline, editorial panel, intelligence feed, post cards (with rationale/sources), reusable components, API service layer, responsive layout, ESLint setup.

**Next:** connect to the live backend so agent data, metrics, publications, and editorial decisions are real instead of demo data.

---

## Vision

Move from a single-shot loop (**prompt → generate**) to a continuous autonomous cycle:

```
Discover → Filter (editorial) → Check memory → Generate → Publish → Remember → Discover again

```

The frontend exists to make this loop visible and easy to monitor.

---

## Contributing

```bash
git checkout -b feature/frontend-change
npm run dev
npm run lint
git add .
git commit -m "feat: update dashboard"
git push origin feature/frontend-change

```

Then open a pull request for review.

## License

Created as part of a hackathon.