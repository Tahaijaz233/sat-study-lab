import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app.database import get_db

with get_db() as conn:
    c = conn.cursor()
    print('Questions:', c.execute('SELECT count(*) FROM questions').fetchone()[0])
    print('Vocab:', c.execute('SELECT count(*) FROM vocab_terms').fetchone()[0])
    print('Courses:', c.execute('SELECT count(*) FROM courses').fetchone()[0])
    print('Modules:', c.execute('SELECT count(*) FROM course_modules').fetchone()[0])
    print()
    print('--- Topics ---')
    for r in c.execute('SELECT section, topic, count(*) FROM questions GROUP BY section, topic ORDER BY section, topic').fetchall():
        print(f"  {r[0]} | {r[1]} | {r[2]}")
    print()
    print('--- Subtopics ---')
    for r in c.execute('SELECT section, topic, subtopic, count(*) FROM questions GROUP BY section, topic, subtopic ORDER BY section, topic, subtopic').fetchall():
        print(f"  {r[0]} | {r[1]} | {r[2]} | {r[3]}")
