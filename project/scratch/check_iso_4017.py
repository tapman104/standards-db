import sqlite3

DB_PATH = r"C:\Users\tapman\Desktop\std db exe\standard.db"

def check_iso_4017():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("\n--- ISO 4017 EQUIVALENTS ---")
    cur.execute("SELECT * FROM equivalents WHERE standard='ISO 4017'")
    for row in cur.fetchall():
        print(row)
    
    conn.close()

if __name__ == "__main__":
    check_iso_4017()
