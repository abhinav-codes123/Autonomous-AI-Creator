import sqlite3
import os

DB_PATH = "autonomous_agent.db"

def clear_runtime_data():
    print(f"Connecting to database at: {os.path.abspath(DB_PATH)}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Safe deletion order based on foreign key relationships
    deletion_order = [
        "post_sources",
        "rejected_topics",
        "posts",
        "topics",
        "agents"
    ]
    
    print("\n=== CLEARING RUNTIME EVALUATION DATA ===")
    for table in deletion_order:
        c.execute(f"DELETE FROM {table};")
        print(f"Cleared table: {table}")
        
    conn.commit()
    
    print("\n=== VERIFYING ROW COUNTS AFTER CLEARING ===")
    all_tables = [t[0] for t in c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    post_clear_counts = {}
    for table in all_tables:
        cnt = c.execute(f"SELECT COUNT(*) FROM '{table}';").fetchone()[0]
        post_clear_counts[table] = cnt
        print(f"  {table:<25}: {cnt}")
        
    # Schema check
    print("\n=== VERIFYING SCHEMA INTEGRITY ===")
    agents_cols = [col[1] for col in c.execute("PRAGMA table_info('agents');").fetchall()]
    print("agents table columns:", agents_cols)
    assert "is_active" in agents_cols, "ERROR: agents.is_active column is missing!"
    print("Schema Check: PASS (agents.is_active exists)")
    
    conn.close()
    return post_clear_counts

if __name__ == "__main__":
    clear_runtime_data()
