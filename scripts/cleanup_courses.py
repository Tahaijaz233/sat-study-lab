import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app.database import get_db

with get_db() as conn:
    c = conn.cursor()
    c.execute("DELETE FROM courses WHERE id IN ('course-rw-1', 'course-math-1')")
    c.execute("DELETE FROM course_modules WHERE course_id IN ('course-rw-1', 'course-math-1')")
    conn.commit()

print("Cleaned up old placeholder courses.")
