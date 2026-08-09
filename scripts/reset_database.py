"""DEVELOPMENT ONLY: Reset the SQLite database."""
import os
import sqlite3
import sys

def main():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'autonomous_agent.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f'Database deleted: {db_path}')
        except Exception as e:
            print(f'Could not delete database file ({e}), truncating tables instead...')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            for table in ["post_sources", "posts", "rejected_topics", "topics", "agents"]:
                try:
                    cursor.execute(f"DELETE FROM {table};")
                except Exception as te:
                    print(f"  Warning deleting table {table}: {te}")
            conn.commit()
            conn.close()
            print('Database tables cleared successfully.')
    else:
        print(f'No database found at: {db_path}')

if __name__ == '__main__':
    main()
