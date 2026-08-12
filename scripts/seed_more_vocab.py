import sqlite3
import datetime
from app.database import get_db
import uuid

def seed_more_vocab():
    new_words = [
        {
            "word": "Alleviate",
            "definition": "Make (suffering, deficiency, or a problem) less severe.",
            "part_of_speech": "verb",
            "difficulty": "Medium",
            "roots_prefixes_suffixes": "ad- (to) + levis (light)",
            "synonyms": "reduce, ease",
            "antonyms": "aggravate, worsen",
            "usage_examples": "He couldn't prevent her pain, only alleviate it.",
            "sentence_completion_drill": "The medicine did nothing to ___ her discomfort."
        },
        {
            "word": "Concur",
            "definition": "Be of the same opinion; agree.",
            "part_of_speech": "verb",
            "difficulty": "Easy",
            "roots_prefixes_suffixes": "com- (together) + currere (to run)",
            "synonyms": "agree, assent",
            "antonyms": "disagree, conflict",
            "usage_examples": "The authors concur with the majority.",
            "sentence_completion_drill": "Do you ___ with my assessment?"
        },
        {
            "word": "Discrepancy",
            "definition": "A lack of compatibility or similarity between two or more facts.",
            "part_of_speech": "noun",
            "difficulty": "Medium",
            "roots_prefixes_suffixes": "dis- (apart) + crepare (to sound)",
            "synonyms": "inconsistency, difference",
            "antonyms": "similarity, correspondence",
            "usage_examples": "There's a discrepancy between your account and his.",
            "sentence_completion_drill": "The auditor found a huge ___ in the financial records."
        },
        {
            "word": "Subjective",
            "definition": "Based on or influenced by personal feelings, tastes, or opinions.",
            "part_of_speech": "adjective",
            "difficulty": "Medium",
            "roots_prefixes_suffixes": "sub- (under) + iacere (to throw)",
            "synonyms": "personal, biased",
            "antonyms": "objective, impartial",
            "usage_examples": "His views are highly subjective.",
            "sentence_completion_drill": "Art appreciation is inherently ___."
        },
        {
            "word": "Objective",
            "definition": "(Of a person or their judgment) not influenced by personal feelings or opinions in considering and representing facts.",
            "part_of_speech": "adjective",
            "difficulty": "Medium",
            "roots_prefixes_suffixes": "ob- (against) + iacere (to throw)",
            "synonyms": "impartial, unbiased",
            "antonyms": "subjective, biased",
            "usage_examples": "Historians try to be objective and impartial.",
            "sentence_completion_drill": "A judge must remain ___ during a trial."
        }
    ]

    with get_db() as conn:
        cursor = conn.cursor()
        for v in new_words:
            # Check if exists
            cursor.execute("SELECT id FROM vocab_terms WHERE term = ?", (v['word'],))
            if cursor.fetchone():
                continue
                
            term_id = f"v_{uuid.uuid4().hex[:10]}"
            cursor.execute("""
                INSERT INTO vocab_terms (
                    id, term, definition, part_of_speech, difficulty, 
                    roots_prefixes_suffixes, synonyms, antonyms, 
                    usage_examples, sentence_completion_drill
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                term_id,
                v['word'],
                v['definition'],
                v['part_of_speech'],
                v['difficulty'],
                v['roots_prefixes_suffixes'],
                v['synonyms'],
                v['antonyms'],
                v['usage_examples'],
                v['sentence_completion_drill']
            ))
            print(f"Added vocabulary: {v['word']}")

if __name__ == "__main__":
    seed_more_vocab()
