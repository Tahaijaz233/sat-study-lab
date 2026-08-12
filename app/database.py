import sqlite3
from contextlib import contextmanager
from app.config import config

def get_connection():
    conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS passages (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT NOT NULL,
            passage_type TEXT,
            word_count INTEGER,
            source_name TEXT,
            source_uri TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS questions (
            id TEXT PRIMARY KEY,
            passage_id TEXT,
            section TEXT NOT NULL,
            topic TEXT NOT NULL,
            subtopic TEXT NOT NULL,
            question_type TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            prompt TEXT NOT NULL,
            answer_explanation TEXT NOT NULL,
            correct_answer_value TEXT,
            source_name TEXT NOT NULL,
            source_uri TEXT,
            import_status TEXT DEFAULT 'active',
            license_notes TEXT,
            content_hash TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (passage_id) REFERENCES passages(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS choices (
            id TEXT PRIMARY KEY,
            question_id TEXT,
            choice_letter TEXT NOT NULL,
            content TEXT NOT NULL,
            is_correct INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS question_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id TEXT,
            tag_name TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS vocab_terms (
            id TEXT PRIMARY KEY,
            word TEXT UNIQUE NOT NULL,
            definition TEXT NOT NULL,
            part_of_speech TEXT,
            difficulty TEXT,
            roots_prefixes_suffixes TEXT,
            synonyms TEXT,
            antonyms TEXT,
            usage_examples TEXT,
            sentence_completion_drill TEXT,
            status TEXT DEFAULT 'unseen',
            repetition_interval INTEGER DEFAULT 1,
            repetition_efactor REAL DEFAULT 2.5,
            repetition_count INTEGER DEFAULT 0,
            next_review_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS practice_sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            section TEXT NOT NULL,
            session_type TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            time_limit_seconds INTEGER NOT NULL,
            time_spent_seconds INTEGER DEFAULT 0,
            score_scaled INTEGER DEFAULT 0,
            status TEXT DEFAULT 'in_progress',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            question_id TEXT,
            selected_choice_id TEXT,
            student_produced_answer TEXT,
            is_correct INTEGER,
            time_spent_seconds INTEGER DEFAULT 0,
            bookmarked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES practice_sessions(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            uri TEXT,
            source_type TEXT NOT NULL,
            permission_notes TEXT,
            question_count INTEGER DEFAULT 0,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            section TEXT NOT NULL,
            description TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS course_modules (
            id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL,
            title TEXT NOT NULL,
            topic TEXT NOT NULL,
            subtopic TEXT NOT NULL,
            lecture_content TEXT NOT NULL,
            order_index INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );

        -- Virtual FTS5 Tables
        CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts USING fts5(
            question_id UNINDEXED, prompt, answer_explanation, topic, subtopic
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS vocab_fts USING fts5(
            vocab_id UNINDEXED, word, definition, roots_prefixes_suffixes
        );

        -- Sync Triggers for questions_fts
        CREATE TRIGGER IF NOT EXISTS questions_ai AFTER INSERT ON questions BEGIN
            INSERT INTO questions_fts(question_id, prompt, answer_explanation, topic, subtopic)
            VALUES (new.id, new.prompt, new.answer_explanation, new.topic, new.subtopic);
        END;

        CREATE TRIGGER IF NOT EXISTS questions_ad AFTER DELETE ON questions BEGIN
            DELETE FROM questions_fts WHERE question_id = old.id;
        END;

        CREATE TRIGGER IF NOT EXISTS questions_au AFTER UPDATE ON questions BEGIN
            DELETE FROM questions_fts WHERE question_id = old.id;
            INSERT INTO questions_fts(question_id, prompt, answer_explanation, topic, subtopic)
            VALUES (new.id, new.prompt, new.answer_explanation, new.topic, new.subtopic);
        END;

        -- Sync Triggers for vocab_fts
        CREATE TRIGGER IF NOT EXISTS vocab_ai AFTER INSERT ON vocab_terms BEGIN
            INSERT INTO vocab_fts(vocab_id, word, definition, roots_prefixes_suffixes)
            VALUES (new.id, new.word, new.definition, new.roots_prefixes_suffixes);
        END;

        CREATE TRIGGER IF NOT EXISTS vocab_ad AFTER DELETE ON vocab_terms BEGIN
            DELETE FROM vocab_fts WHERE vocab_id = old.id;
        END;

        CREATE TRIGGER IF NOT EXISTS vocab_au AFTER UPDATE ON vocab_terms BEGIN
            DELETE FROM vocab_fts WHERE vocab_id = old.id;
            INSERT INTO vocab_fts(vocab_id, word, definition, roots_prefixes_suffixes)
            VALUES (new.id, new.word, new.definition, new.roots_prefixes_suffixes);
        END;
        ''')
