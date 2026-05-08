import sqlite3

DB_PATH = r"C:\Users\tapman\Desktop\std db exe\standard.db"

def list_standards_with_props():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT standard FROM mechanical_properties")
    standards = [r[0] for r in cur.fetchall()]
    print(f"Standards with properties ({len(standards)}):")
    for s in standards:
        print(f" - {s}")
    conn.close()

if __name__ == "__main__":
    list_standards_with_props()
