import sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

db_path=ROOT/"backend"/"database"/"insights.db"
schema_path=ROOT/"backend"/"database"/"schema.sql"

conn=sqlite3.connect(db_path)

with open(schema_path,"r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Db initialized")