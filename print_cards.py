import sqlite3

conn = sqlite3.connect('sat_lab.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

def print_q(qid, card_label):
    r = c.execute("SELECT q.*, p.content as passage FROM questions q LEFT JOIN passages p ON q.passage_id = p.id WHERE q.id = ?", (qid,)).fetchone()
    choices = c.execute("SELECT choice_letter, content, is_correct FROM choices WHERE question_id = ? ORDER BY choice_letter", (qid,)).fetchall()
    print(f"=== {card_label} ===")
    print("ID:", r['id'])
    print("Subtopic:", r['subtopic'])
    print("Passage:", r['passage'])
    print("Prompt:", r['prompt'])
    print("Choices:")
    for ch in choices:
        flag = "[CORRECT]" if ch['is_correct'] else ""
        print(f"  {ch['choice_letter']}) {ch['content']} {flag}")
    print()

print_q("93d30f6a-9bd2-4c6b-9fef-aa9966598409", "Card 27 (in R&W filter)")
print_q("c37049e7-e5e4-4b0e-b5b2-59d52bdbc50e", "Card 42 (in R&W filter)")

conn.close()
