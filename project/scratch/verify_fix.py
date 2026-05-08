import sqlite3

DB_PATH = r"C:\Users\tapman\Desktop\std db exe\standard.db"

def verify_fix():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("--- MECHANICAL PROPERTIES ---")
    cur.execute("SELECT * FROM mechanical_properties LIMIT 10")
    for row in cur.fetchall():
        print(row)
    
    print("\n--- DIN 933 EQUIVALENTS ---")
    cur.execute("SELECT * FROM equivalents WHERE standard='DIN 933'")
    for row in cur.fetchall():
        print(row)
    
    conn.close()

if __name__ == "__main__":
    verify_fix()
