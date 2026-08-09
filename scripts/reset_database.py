"""DEVELOPMENT ONLY: Reset the SQLite database."""
import os
import sys

def main():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'autonomous_agent.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f'Database deleted: {db_path}')
    else:
        print(f'No database found at: {db_path}')

if __name__ == '__main__':
    main()
