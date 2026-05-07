import sqlite3
from pathlib import Path

DB_PATH = Path("fasteners.db")

def verify():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("--- Table Counts ---")
    tables = ["standards", "equivalents", "waf_conflicts"]
    for table in tables:
        cursor.execute(f"SELECT count(*) FROM {table}")
        print(f"{table}: {cursor.fetchone()[0]}")
    
    print("\n--- Sample Equivalents (GOST 7798-70) ---")
    cursor.execute("""
        SELECT target_standard, target_body 
        FROM equivalents 
        WHERE source_id = 'gost_7798_70'
    """)
    for row in cursor.fetchall():
        print(f"Equivalent: {row[0]} ({row[1]})")
        
    print("\n--- Testing FTS5 Rank ---")
    cursor.execute("""
        SELECT standard_no, rank 
        FROM standards_fts 
        WHERE standards_fts MATCH 'ISO 4014' 
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"Standard: {row[0]}, Rank: {row[1]}")

    print("\n--- Testing Trigger (Insert/Search) ---")
    try:
        cursor.execute("INSERT INTO standards (id, standard_no, title, body, country, category) VALUES ('test_id', 'TEST-999', 'Self-Sealing Stem Bolt', 'FALCON', 'Deep Space 9', 'bolt')")
        cursor.execute("SELECT standard_no FROM standards_fts WHERE standards_fts MATCH 'Stem'")
        result = cursor.fetchone()
        if result:
            print(f"Trigger Test Success: Found '{result[0]}'")
        else:
            print("Trigger Test Failed: Could not find inserted record in FTS")
        conn.rollback() # Don't keep the test data
    except Exception as e:
        print(f"Trigger Test Error: {e}")

    conn.close()

if __name__ == "__main__":
    verify()
