import uuid
import sqlite3
from app.database import get_db

def seed_courses():
    courses = [
        {
            "id": "course-rw-1",
            "title": "Digital SAT Reading & Writing Mastery",
            "section": "Reading and Writing",
            "description": "A comprehensive prebuilt course covering all domains of the Reading and Writing section."
        },
        {
            "id": "course-math-1",
            "title": "Digital SAT Math Mastery",
            "section": "Math",
            "description": "Master Algebra, Advanced Math, Problem Solving, and Geometry."
        }
    ]

    modules = [
        {
            "id": "mod-rw-1",
            "course_id": "course-rw-1",
            "title": "Information and Ideas: Central Ideas and Details",
            "topic": "Information and Ideas",
            "subtopic": "Central Ideas and Details",
            "order_index": 1,
            "lecture_content": """# Central Ideas and Details
These questions ask you to identify the main point or central idea of a text.

**Strategies:**
1. **Read actively:** Summarize the text in your own words before looking at the choices.
2. **Beware of too broad/too narrow:** Incorrect choices often state something that is true but not the *main* idea, or they go beyond what the text supports.
3. **Check the conclusion:** The central idea is often synthesized in the final sentence.
"""
        },
        {
            "id": "mod-rw-2",
            "course_id": "course-rw-1",
            "title": "Craft and Structure: Words in Context",
            "topic": "Craft and Structure",
            "subtopic": "Words in Context",
            "order_index": 2,
            "lecture_content": """# Words in Context
These questions test your ability to determine the meaning of vocabulary words based on how they are used in a sentence.

**Strategies:**
1. **Cover the word:** Pretend the word is a blank and guess what word you would use.
2. **Look for context clues:** Authors often provide definitions, synonyms, or antonyms in the surrounding sentences.
3. **Plug it in:** Test each answer choice in the sentence to see which one makes the most logical sense.
"""
        },
        {
            "id": "mod-math-1",
            "course_id": "course-math-1",
            "title": "Algebra: Linear Equations",
            "topic": "Algebra",
            "subtopic": "Linear Equations in One Variable",
            "order_index": 1,
            "lecture_content": """# Linear Equations in One Variable
A linear equation in one variable can be written in the form $ax + b = c$.

**Strategies:**
1. **Isolate the variable:** Use inverse operations to get $x$ by itself.
2. **Use Desmos:** You can graph the left side as $y = ax + b$ and the right side as $y = c$ to find the intersection!
3. **Check your work:** Plug your answer back into the original equation.
"""
        }
    ]

    with get_db() as conn:
        for course in courses:
            conn.execute(
                "INSERT OR REPLACE INTO courses (id, title, section, description) VALUES (?, ?, ?, ?)",
                (course['id'], course['title'], course['section'], course['description'])
            )
            
        for module in modules:
            conn.execute(
                "INSERT OR REPLACE INTO course_modules (id, course_id, title, topic, subtopic, lecture_content, order_index) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (module['id'], module['course_id'], module['title'], module['topic'], module['subtopic'], module['lecture_content'], module['order_index'])
            )
            
    print("Courses and modules seeded successfully!")

if __name__ == "__main__":
    seed_courses()
