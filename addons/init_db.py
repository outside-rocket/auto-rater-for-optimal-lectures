import sqlite3

conn=sqlite3.connect("teachers.db")
cur=conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS teachers(
name TEXT PRIMARY KEY,

clarity_sum REAL DEFAULT 0,
clarity_count INTEGER DEFAULT 0,

assignment_sum REAL DEFAULT 0,
assignment_count INTEGER DEFAULT 0,

leniency_sum REAL DEFAULT 0,
leniency_count INTEGER DEFAULT 0,

strictness_sum REAL DEFAULT 0,
strictness_count INTEGER DEFAULT 0,

comments TEXT DEFAULT '',

last_updated TEXT
)
""")

conn.commit()
conn.close()

print("database created")