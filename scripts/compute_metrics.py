import sqlite3
from datetime import datetime

DB_PATH = "autonomous_agent.db"
AGENT_ID = "3a77a6987f1e498c892b07be8552812f"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

posts = c.execute("SELECT id, text, rationale, created_at FROM posts WHERE agent_id=? ORDER BY created_at ASC", (AGENT_ID,)).fetchall()

timestamps = [datetime.fromisoformat(p[3]) for p in posts]

print("Post timestamps:")
for i, ts in enumerate(timestamps, 1):
    print(f"Post {i}: {ts.isoformat()}")

intervals = [(timestamps[i] - timestamps[i-1]).total_seconds() for i in range(1, len(timestamps))]
print("\nIntervals between consecutive posts (seconds):")
for i, inv in enumerate(intervals, 1):
    print(f"Cycle {i} to {i+1}: {inv:.2f}s")

print(f"\nAverage Interval: {sum(intervals)/len(intervals):.2f}s")
print(f"Min Interval: {min(intervals):.2f}s")
print(f"Max Interval: {max(intervals):.2f}s")

conn.close()
