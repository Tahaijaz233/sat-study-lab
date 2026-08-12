import sqlite3

conn = sqlite3.connect('sat_lab.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# All questions in default view order
all_qs = c.execute("""
    SELECT q.id, q.section, q.subtopic, q.prompt, p.content as passage 
    FROM questions q 
    LEFT JOIN passages p ON q.passage_id = p.id 
    WHERE q.import_status = 'active' 
    ORDER BY q.created_at DESC
""").fetchall()

matches_all = []
for idx, q in enumerate(all_qs, 1):
    content = (q['passage'] or '') + ' ' + (q['prompt'] or '')
    if '___' in content or '______' in content:
        matches_all.append((idx, q['id'], q['subtopic'], q['section']))

print("FIRST 5 IN ALL QUESTIONS VIEW:")
for m in matches_all[:5]:
    print(f"Card {m[0]} of {len(all_qs)} | ID: {m[1]} | Section: {m[3]} | Subtopic: {m[2]}")

# Reading & Writing filter view
rw_qs = [q for q in all_qs if q['section'] == 'Reading & Writing']
matches_rw = []
for idx, q in enumerate(rw_qs, 1):
    content = (q['passage'] or '') + ' ' + (q['prompt'] or '')
    if '___' in content or '______' in content:
        matches_rw.append((idx, q['id'], q['subtopic']))

print("\nFIRST 5 IN READING & WRITING FILTER VIEW:")
for m in matches_rw[:5]:
    print(f"Card {m[0]} of {len(rw_qs)} | ID: {m[1]} | Subtopic: {m[2]}")

conn.close()
