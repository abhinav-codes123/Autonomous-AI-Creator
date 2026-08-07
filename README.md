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

1. **Autonomous Background Scheduler (`APScheduler`)**:
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
