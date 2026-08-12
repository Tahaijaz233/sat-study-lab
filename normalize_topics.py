import sqlite3

conn = sqlite3.connect('sat_lab.db')
c = conn.cursor()

# Normalize the hyphenated variant
c.execute("UPDATE questions SET topic = 'Problem Solving and Data Analysis' WHERE topic = 'Problem-Solving and Data Analysis'")
print('Rows updated:', c.rowcount)

# Verify
rows = c.execute("SELECT DISTINCT topic FROM questions WHERE section = 'Math'").fetchall()
print('Math topics:', [r[0] for r in rows])

rows = c.execute("SELECT DISTINCT topic FROM questions WHERE section = 'Reading & Writing'").fetchall()
print('RW topics:', [r[0] for r in rows])

# Count by topic and difficulty
print('\n--- Math Distribution ---')
for row in c.execute("SELECT topic, difficulty, COUNT(*) as cnt FROM questions WHERE section = 'Math' AND import_status = 'active' GROUP BY topic, difficulty ORDER BY topic, difficulty").fetchall():
    print(f"  {row[0]} | {row[1]}: {row[2]}")

print('\n--- RW Distribution ---')
for row in c.execute("SELECT topic, difficulty, COUNT(*) as cnt FROM questions WHERE section = 'Reading & Writing' AND import_status = 'active' GROUP BY topic, difficulty ORDER BY topic, difficulty").fetchall():
    print(f"  {row[0]} | {row[1]}: {row[2]}")

conn.commit()
conn.close()
