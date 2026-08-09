import sqlite3

DB_PATH = "autonomous_agent.db"
AGENT_ID = "3a77a6987f1e498c892b07be8552812f"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

posts = c.execute("SELECT id, text, rationale, created_at FROM posts WHERE agent_id=? ORDER BY created_at ASC", (AGENT_ID,)).fetchall()

print("--- POST ANALYSIS ---")
for i, p in enumerate(posts, 1):
    pid, text, rat, cat = p
    first_line = text.split("\n\n")[1] if "\n\n" in text else text[:100]
    print(f"Cycle {i}:")
    print(f"  Post ID: {pid}")
    print(f"  Timestamp: {cat}")
    print(f"  Extract: {first_line}")
    print(f"  Rationale: {rat[:150]}...")
    print()

# Check topics rejected per reason
rejections = c.execute("SELECT reason, COUNT(*) FROM rejected_topics WHERE topic_id IN (SELECT id FROM topics WHERE agent_id=?) GROUP BY reason", (AGENT_ID,)).fetchall()
print("--- REJECTION REASONS ---")
for r, cnt in rejections:
    print(f"  {r}: {cnt}")

conn.close()
