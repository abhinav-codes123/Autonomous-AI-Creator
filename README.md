# Autonomous AI Creator — Full-Stack Technical Intelligence System

An autonomous AI and technology persona system built for the **ABTalks Vibe Code Hackathon (PS3 — Autonomous AI Creator)**.

After a single initialization request, the agent independently monitors live information feeds, editorially filters content, enforces memory deduplication, maintains persona consistency, and continuously publishes technical intelligence over time — **without requiring any further human prompts**.

---

## Key Features

- **Single Initialization Architecture**: Receives persona details (`name`, `domain`) once via `POST /api/agent/init`, then runs autonomously in the background via APScheduler.
- **Live Multi-Source Discovery**: Continuously monitors live data from Hacker News, GitHub Search & Trending, arXiv papers, and AI engineering blogs (OpenAI, Anthropic, DeepMind, TechCrunch).
- **Multi-Dimensional Editorial Engine**: Evaluates topics across 6 criteria (Importance, Novelty, Credibility, Persona Fit, Recency, Similarity Penalty) and persists explicit rejection reasons (`Clickbait`, `Too promotional`, `Already discussed`, `Low relevance`, `Old news`).
- **Memory & Deduplication**: Prevents duplicate stories and exact URL repetition using sequence similarity algorithms and historical database persistence.
- **Transparent Rationale & Source Citations**: Every published post includes 3-part editorial reasoning (Why selected, Why relevant now, Why chosen over alternatives) alongside verified source URLs.
- **Read-Only Evaluator Feed**: `GET /api/agent/feed?agentId=<uuid>` strictly queries the database without triggering side-effect content generation.
- **Real-Time React Dashboard**: Modern UI displaying live stats (`GET /api/agent/stats`), live scanning indicators, activity timeline, editorial decision breakdowns, and post cards with + New Agent session reset controls.

---

## Architecture Overview

```
                          ┌──────────────────────────┐
                          │   React + Vite Dashboard │
                          └────────────┬─────────────┘
                                       │ HTTP API
                                       ▼
                          ┌──────────────────────────┐
                          │   FastAPI Web Server     │
                          └────────────┬─────────────┘
                                       │
                ┌──────────────────────┼──────────────────────┐
                │                      │                      │
                ▼                      ▼                      ▼
    ┌──────────────────────┐ ┌──────────────────┐ ┌────────────────────────┐
    │  Topic Discovery     │ │ Editorial Engine │ │  Memory Engine         │
    │  (HN, GitHub, arXiv) │ │ (6-Factor Score) │ │  (Similarity Check)    │
    └──────────────────────┘ └──────────────────┘ └────────────────────────┘
                │                      │                      │
                └──────────────────────┼──────────────────────┘
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │  Publishing Service      │
                          └────────────┬─────────────┘
                                       │
                                       ▼
                          ┌──────────────────────────┐
                          │ Async ORM (DB Persistence)│
                          └──────────────────────────┘
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+ and `npm`

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/abhinav-codes123/Autonomous-AI-Creator.git
cd Autonomous-AI-Creator

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

For an existing development database created before agent-scoped topics, migrate
it before starting the server:

```bash
alembic upgrade head
# or, for disposable development data only:
python scripts/reset_database.py
```

The API will be live at `http://localhost:8000`. OpenAPI documentation is available at `http://localhost:8000/docs`.

### 2. Frontend Setup

In a new terminal window:

```bash
# Install frontend dependencies
npm install

# Start the Vite development server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser to access the live dashboard.

---

## API Documentation

### 1. Initialize Agent Persona
**Endpoint**: `POST /api/agent/init`

**Request Body**:
```json
{
  "persona": {
    "name": "Ada",
    "domain": "AI Security"
  }
}
```

**Response** (`200 OK`):
```json
{
  "agentId": "5f0ce850-b0c3-49b4-a5a9-d80e2fff1a4e"
}
```

---

### 2. Retrieve Agent Feed (Read-Only)
**Endpoint**: `GET /api/agent/feed?agentId=<uuid>`

**Response** (`200 OK`):
```json
{
  "posts": [
    {
      "id": "aaeb7d49-fe84-4860-91de-ce8cf0ef7ef7",
      "createdAt": "2026-08-08T14:27:11.385000Z",
      "text": "Technical Analysis of 'Build a minimal clone of OpenAI’s Canvas, Operator'...",
      "rationale": "Why Selected: High technical significance...\nWhy Relevant Now: Fresh discovery...\nWhy Chosen Over Alternatives: Outscored 19 alternative candidates.",
      "sources": [
        "https://news.ycombinator.com/item?id=123456"
      ]
    }
  ]
}
```

---

### 3. Retrieve Live Agent Statistics
**Endpoint**: `GET /api/agent/stats?agentId=<uuid>`

**Response** (`200 OK`):
```json
{
  "sourcesMonitored": 8,
  "topicsDiscovered": 45,
  "topicsRejected": 43,
  "published": 2,
  "shortlisted": 2,
  "selected": 2
}
```

---

## Testing & Verification

Run the automated test suite covering API routes, discovery providers, editorial scoring, memory deduplication, and end-to-end cycle execution:

```bash
.venv/bin/pytest -v
```

---

## Deployment to Render

### 1. Create PostgreSQL Database on Render
1. Go to your [Render Dashboard](https://dashboard.render.com/) and click **New +** → **PostgreSQL**.
2. Set a name (e.g. `autonomous-ai-db`) and select the Free instance tier.
3. Click **Create Database**.
4. Once created, copy the **Internal Database URL** (or External Database URL if deploying from outside Render's network).

### 2. Create Web Service on Render
1. In Render Dashboard, click **New +** → **Web Service**.
2. Connect your GitHub repository: `abhinav-codes123/Autonomous-AI-Creator`.
3. Select **Python** as the runtime.

### 3. Configure Build & Start Commands
- **Build Command**:
  ```bash
  pip install -r requirements.txt && alembic upgrade head
  ```
- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

### 4. Configure Environment Variables
In the Web Service **Environment** section, add the following variables:

| Key | Example / Value | Description |
|---|---|---|
| `DATABASE_URL` | `postgres://user:pass@ep-host.render.com/dbname` | Render PostgreSQL Connection String (automatically converted to `postgresql+asyncpg://` by backend) |
| `LLM_PROVIDER` | `mock` or `openai` | Set to `mock` for free offline mode, or `openai` for OpenAI API |
| `OPENAI_API_KEY` | `sk-...` | Optional if using `LLM_PROVIDER=openai` |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI Model selection |
| `SCHEDULER_INTERVAL_MINUTES` | `1` | Interval between autonomous background cycles in minutes |

### 5. Health Check & API Verification
- **Health Check Endpoint**: `GET /health` (returns `{"status": "ok", "project": "Autonomous AI Persona Backend"}`)
- **Agent Initialization**: `POST /api/agent/init`
- **Agent Feed Monitoring**: `GET /api/agent/feed?agentId=<agentId>`

---

## License

Developed for the ABTalks Vibe Code Hackathon (PS3 — Autonomous AI Creator).
