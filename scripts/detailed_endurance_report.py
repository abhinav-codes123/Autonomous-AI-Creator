import sqlite3

DB_PATH = "autonomous_agent.db"
AGENT_ID = "3a77a6987f1e498c892b07be8552812f"

def analyze():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    posts = c.execute("SELECT id, text, rationale, created_at FROM posts WHERE agent_id=? ORDER BY created_at ASC", (AGENT_ID,)).fetchall()
    
    print(f"Total Posts: {len(posts)}")
    for i, p in enumerate(posts, 1):
        pid, text, rat, cat = p
        title = text.split("\n\n")[1] if "\n\n" in text else text[:60]
        print(f"\n--- Post {i} ---")
        print(f"ID: {pid}")
        print(f"Created At: {cat}")
        print(f"Title/Subject: {title}")
        print(f"Rationale: {rat}")

    # Analyze topics
    topics = c.execute("SELECT id, title, status, score, discovered_at FROM topics WHERE agent_id=? ORDER BY discovered_at ASC", (AGENT_ID,)).fetchall()
    print(f"\nTotal Topics in DB: {len(topics)}")
    
    rejected = c.execute("SELECT id, topic_id, reason FROM rejected_topics WHERE topic_id IN (SELECT id FROM topics WHERE agent_id=?)", (AGENT_ID,)).fetchall()
    print(f"Total Rejected Topics Records: {len(rejected)}")
    
    conn.close()

if __name__ == "__main__":
    analyze()
