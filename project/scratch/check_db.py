import sqlite3
import pathlib
import re
import yaml

DB_PATH = r"C:\Users\tapman\Desktop\std db exe\standard.db"
STANDARDS_ROOT = pathlib.Path(r"C:\Users\tapman\Desktop\standards db\project\domains\mechanical\fasteners")

def check_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("--- DB STATS ---")
    cur.execute("SELECT COUNT(*) FROM standards")
    print(f"Standards: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM equivalents")
    print(f"Equivalents: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM mechanical_properties")
    print(f"Mechanical Properties: {cur.fetchone()[0]}")
    
    print("\n--- DIN 933 EQUIVALENTS ---")
    cur.execute("SELECT * FROM equivalents WHERE standard='DIN 933'")
    for row in cur.fetchall():
        print(row)
    
    print("\n--- STANDARDS FOR DIN 933 ---")
    cur.execute("SELECT standard, body FROM standards WHERE standard='DIN 933'")
    for row in cur.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    check_db()
