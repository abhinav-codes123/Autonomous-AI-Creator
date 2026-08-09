import time
import sqlite3
import httpx
from datetime import datetime, timezone

AGENT_ID = "3a77a698-7f1e-498c-892b-07be8552812f"
DB_PATH = "autonomous_agent.db"

def get_db_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT id, title, status, score, discovered_at FROM topics WHERE agent_id = ? ORDER BY discovered_at ASC", (AGENT_ID,))
    topics = c.fetchall()
    
    c.execute("SELECT id, text, rationale, created_at FROM posts WHERE agent_id = ? ORDER BY created_at ASC", (AGENT_ID,))
    posts = c.fetchall()
    
    conn.close()
    return topics, posts

def get_feed_count():
    try:
        r = httpx.get(f"http://127.0.0.1:8000/api/agent/feed?agentId={AGENT_ID}", timeout=5.0)
        if r.status_code == 200:
            return len(r.json().get("posts", []))
    except Exception as e:
        print("Error getting feed:", e)
    return 0

def monitor():
    print(f"Monitoring Agent {AGENT_ID} for 11 minutes (11 cycles)...")
    start_time = time.time()
    last_post_count = 0
    
    while time.time() - start_time < 670:
        topics, posts = get_db_stats()
        feed_count = get_feed_count()
        now_str = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(f"[{now_str}] DB Topics: {len(topics)} | DB Posts: {len(posts)} | Feed API Posts: {feed_count}")
        time.sleep(10)

if __name__ == "__main__":
    monitor()
