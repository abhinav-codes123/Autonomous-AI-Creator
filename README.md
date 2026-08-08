# Autonomous AI Persona & Content Creator Dashboard

A production-quality, full-stack autonomous AI content creator application featuring a **FastAPI (Python 3.12+) Backend** and a **React + Vite Dashboard Frontend**.

The system operates autonomously without human prompts after initialization. The background pipeline continuously discovers trending tech topics, evaluates them via an Editorial Engine, checks memory history in PostgreSQL/SQLite for deduplication, synthesizes persona-aligned commentary via LLM abstractions, and serves real-time updates to an interactive web dashboard.

---

## 🌟 Full-Stack Architecture

```
                               ┌────────────────────────────────────────┐
                               │   React + Vite Frontend Dashboard      │
                               │  (Live Feed, Editorial Scores, Status) │
                               └───────────────────┬────────────────────┘
                                                   │ HTTP / REST
                                                   ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              FastAPI Backend (Python 3.12+)                            │
│                                                                                        │
│  ┌─────────────────────────┐      ┌──────────────────────┐      ┌──────────────────┐   │
│  │   POST /api/agent/init  │──────►  Autonomous Scheduler │ ───► │ Topic Discovery  │   │
│  │   GET  /api/agent/feed  │      │     (APScheduler)    │      │ (HN, GitHub,     │   │
│  └─────────────────────────┘      └──────────────────────┘      │  arXiv, RSS)     │   │
│                                                                 └─────────┬────────┘   │
│                                                                           │            │
│  ┌─────────────────────────┐      ┌──────────────────────┐                ▼            │
│  │   LLM Provider Layer    │ ◄────┤   Prompt Builder     │      ┌──────────────────┐   │
│  │ (OpenAI / Free Mock)    │      │(Persona & Style Rules│ ◄─── │ Editorial Engine │   │
│  └────────────┬────────────┘      └──────────────────────┘      │(Scoring & Rules) │   │
│               │                                                 └─────────▲────────┘   │
│               ▼                                                           │            │
│  ┌─────────────────────────┐                                    ┌─────────┴────────┐   │
│  │   PostgreSQL / SQLite   │◄───────────────────────────────────┤  Memory Engine   │   │
│  │   (Persisted Posts)     │                                    │  (Deduplication) │   │
│  └─────────────────────────┘                                    └──────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

### 🖥️ Frontend Dashboard (React + Vite)
- **Interactive Agent Initialization**: Initialize personas (e.g., Ada in AI Security) dynamically.
- **Real-Time Feed**: View autonomously generated technical posts with expandable selection rationales and direct source links.
- **Editorial Judgment Panel**: Visual breakdown of topic evaluation scores across Importance, Novelty, Credibility, Persona Fit, Recency, and Penalty dimensions.
- **Live Activity Log & Metrics**: Real-time status indicators, agent health, and discovery source breakdown.
- **Dark Mode Aesthetic**: Sleek design built with glassmorphism, responsive cards, and clean typography.

### ⚙️ Backend & Autonomous Core (FastAPI & Python 3.12+)
- **Instant Initialization Response**: `POST /api/agent/init` creates agent records and synchronously generates the first post so `GET /feed` is populated immediately.
- **Autonomous Background Scheduler (`APScheduler`)**: Runs periodic content generation cycles every 30 minutes without human intervention.
- **Multi-Source Topic Discovery**:
  - Hacker News API
  - GitHub Trending Repositories
  - arXiv Research Papers API
  - RSS Feeds (OpenAI, Anthropic, DeepMind, TechCrunch)
  - Offline Domain Fallback Provider
- **Editorial Engine**:
  - Evaluates topics across 6 criteria: *Importance*, *Novelty*, *Credibility*, *Persona Fit*, *Recency*, and *Duplicate Penalty*.
  - Filters clickbait, promotional spam (word-boundary matched), and low-relevance topics.
  - Persists rejected topics with explicit rejection reasons.
- **Memory Engine**:
  - Tracks published posts, covered topics, and keywords in PostgreSQL/SQLite.
  - Employs Jaccard & Sequence matcher text similarity algorithms to prevent duplicate content.
- **Persona Engine**:
  - Dynamic domain profiling for any tech domain (defaults to **AI Security** with keywords like *Prompt Injection*, *Red Teaming*, *CVEs*, *LLM Security*).
  - Enforces strict writing guidelines (No emojis, No hype, Technical precision).
- **Pluggable LLM Abstraction Layer**:
  - Supports OpenAI API (`gpt-4o`, `gpt-4o-mini`).
  - Includes a 100% free built-in `MockLLMProvider` for offline execution and testing without API key costs.

---

## 📡 API Endpoints

### 1. Initialize Agent
- **Method**: `POST /api/agent/init`
- **Request Body**:
  ```json
  {
    "persona": {
      "name": "Ada",
      "domain": "AI Security"
    }
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "agentId": "acb1f79f-0c9f-4f81-aaec-a43b4f9a0ebf"
  }
  ```

### 2. Retrieve Agent Feed
- **Method**: `GET /api/agent/feed?agentId=acb1f79f-0c9f-4f81-aaec-a43b4f9a0ebf`
- **Response** (200 OK - Newest First):
  ```json
  {
    "posts": [
      {
        "id": "eb472147-197e-4074-b52b-67ee83c448d3",
        "createdAt": "2026-08-08T13:11:24.904481+00:00",
        "text": "Technical Analysis of 'Build a minimal clone of OpenAI’s Canvas, Operator'...",
        "rationale": "Selection Rationale:\n1. Why selected...\n2. Why relevant now...\n3. Why chosen over alternatives...",
        "sources": [
          "https://news.ycombinator.com/item?id=43232049"
        ]
      }
    ]
  }
  ```

---

## 🛠️ Quickstart & Local Setup

### Prerequisites
- **Python 3.12+**
- **Node.js 18+** & npm

### 1. Backend Setup & Startup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```
Backend API interactive docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 2. Frontend Setup & Startup
In a new terminal window:
```bash
# Install frontend dependencies
npm install

# Start Vite dev server
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser to view the interactive dashboard.

---

## 🐳 Docker Deployment

To launch the full backend service alongside a PostgreSQL 16 database using Docker Compose:

```bash
docker-compose up --build
```
Alembic migrations will automatically apply on container startup.

---

## 🧪 Testing

Run the automated test suite covering API routes, discovery providers, editorial scoring, memory deduplication, and end-to-end cycle execution:

```bash
.venv/bin/pytest -v
```
