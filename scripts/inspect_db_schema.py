import sqlite3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings

def inspect_db():
    print("=== DATABASE CONFIGURATION ===")
    print("Settings DATABASE_URL:", settings.DATABASE_URL)
    db_path = "autonomous_agent.db"
    print(f"Absolute Database Path: {os.path.abspath(db_path)}")
    print(f"Database File Exists: {os.path.exists(db_path)}")
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    print("\n=== TABLES IN DATABASE ===")
    tables = [t[0] for t in c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    print("Tables found:", tables)
    
    print("\n=== TABLE SCHEMAS & FOREIGN KEYS ===")
    for table in tables:
        print(f"\n--- Table: {table} ---")
        columns = c.execute(f"PRAGMA table_info('{table}');").fetchall()
        print("  Columns:")
        for col in columns:
            cid, name, ctype, notnull, dflt_value, pk = col
            print(f"    - {name} ({ctype}) | NotNull: {notnull} | Default: {dflt_value} | PK: {pk}")
        
        fks = c.execute(f"PRAGMA foreign_key_list('{table}');").fetchall()
        if fks:
            print("  Foreign Keys:")
            for fk in fks:
                id_, seq, to_table, from_col, to_col, on_update, on_delete, match = fk
                print(f"    - {table}.{from_col} -> {to_table}.{to_col} (On Delete: {on_delete})")
        else:
            print("  Foreign Keys: None")

    print("\n=== ROW COUNTS BEFORE CLEARING ===")
    counts = {}
    for table in tables:
        cnt = c.execute(f"SELECT COUNT(*) FROM '{table}';").fetchone()[0]
        counts[table] = cnt
        print(f"  {table:<25}: {cnt}")
        
    conn.close()

if __name__ == "__main__":
    inspect_db()
