"""Database connection and schema helpers.

SQLite remains the zero-configuration local default.  When ``DATABASE_URL`` is
set, the same application code is backed by PostgreSQL.  The lightweight
compatibility wrappers below keep the DB-API surface used by the routers
(``?`` parameters and ``INSERT OR IGNORE``) portable between both engines.
"""

import re
import sqlite3
from contextlib import contextmanager
from typing import Any, Optional, Sequence

from app.config import config


class PostgresCursor:
    """Translate the small SQLite SQL subset used by the application."""

    def __init__(self, cursor):
        self._cursor = cursor

    @staticmethod
    def _translate(sql: str) -> str:
        translated = sql.replace("?", "%s")

        # Seed/import scripts use SQLite's convenient INSERT OR IGNORE/REPLACE
        # forms. PostgreSQL expresses the idempotent behavior with ON CONFLICT.
        if re.search(r"\bINSERT\s+OR\s+(?:IGNORE|REPLACE)\b", translated, re.IGNORECASE):
            translated = re.sub(
                r"\bINSERT\s+OR\s+(?:IGNORE|REPLACE)\b", "INSERT", translated,
                count=1, flags=re.IGNORECASE,
            )
            stripped = translated.rstrip()
            had_semicolon = stripped.endswith(";")
            if had_semicolon:
                stripped = stripped[:-1].rstrip()
            translated = stripped + " ON CONFLICT DO NOTHING"
            if had_semicolon:
                translated += ";"

        return translated

    def execute(self, sql: str, params: Optional[Sequence[Any]] = None):
        translated = self._translate(sql)
        if params is None:
            self._cursor.execute(translated)
        else:
            self._cursor.execute(translated, params)
        return self

    def executemany(self, sql: str, params_seq):
        self._cursor.executemany(self._translate(sql), params_seq)
        return self

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    @property
    def rowcount(self):
        return self._cursor.rowcount

    def close(self):
        self._cursor.close()


class PostgresConnection:
    """Expose the sqlite3-style methods used throughout the application."""

    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return PostgresCursor(self._connection.cursor())

    def execute(self, sql: str, params: Optional[Sequence[Any]] = None):
        return self.cursor().execute(sql, params)

    def executescript(self, script: str):
        # PostgreSQL/psycopg2 accepts a schema containing multiple statements.
        cursor = self._connection.cursor()
        try:
            cursor.execute(script)
        finally:
            cursor.close()

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def close(self):
        self._connection.close()


SQLITE_SCHEMA = r'''
CREATE TABLE IF NOT EXISTS passages (
    id TEXT PRIMARY KEY,
    title TEXT,
    content TEXT NOT NULL,
    passage_type TEXT,
    word_count INTEGER,
    source_name TEXT,
    source_uri TEXT,
    content_hash TEXT UNIQUE,
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

CREATE VIRTUAL TABLE IF NOT EXISTS questions_fts USING fts5(
    question_id UNINDEXED, prompt, answer_explanation, topic, subtopic
);

CREATE VIRTUAL TABLE IF NOT EXISTS vocab_fts USING fts5(
    vocab_id UNINDEXED, word, definition, roots_prefixes_suffixes
);

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
'''


POSTGRES_SCHEMA = r'''
CREATE TABLE IF NOT EXISTS passages (
    id TEXT PRIMARY KEY,
    title TEXT,
    content TEXT NOT NULL,
    passage_type TEXT,
    word_count INTEGER,
    source_name TEXT,
    source_uri TEXT,
    content_hash TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    passage_id TEXT REFERENCES passages(id) ON DELETE CASCADE,
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS choices (
    id TEXT PRIMARY KEY,
    question_id TEXT REFERENCES questions(id) ON DELETE CASCADE,
    choice_letter TEXT NOT NULL,
    content TEXT NOT NULL,
    is_correct INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS question_tags (
    id BIGSERIAL PRIMARY KEY,
    question_id TEXT REFERENCES questions(id) ON DELETE CASCADE,
    tag_name TEXT NOT NULL
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
    repetition_efactor DOUBLE PRECISION DEFAULT 2.5,
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
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT REFERENCES practice_sessions(id) ON DELETE CASCADE,
    question_id TEXT REFERENCES questions(id) ON DELETE CASCADE,
    selected_choice_id TEXT,
    student_produced_answer TEXT,
    is_correct INTEGER,
    time_spent_seconds INTEGER DEFAULT 0,
    bookmarked INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    course_id TEXT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    subtopic TEXT NOT NULL,
    lecture_content TEXT NOT NULL,
    order_index INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS questions_section_idx ON questions(section);
CREATE INDEX IF NOT EXISTS questions_topic_idx ON questions(topic);
CREATE INDEX IF NOT EXISTS choices_question_idx ON choices(question_id);
CREATE INDEX IF NOT EXISTS attempts_session_idx ON user_attempts(session_id);
'''


def is_postgres() -> bool:
    return bool(config.DATABASE_URL)


def get_connection():
    if is_postgres():
        try:
            import psycopg2
            from psycopg2.extras import DictCursor
        except ImportError as exc:  # pragma: no cover - depends on deployment env
            raise RuntimeError(
                "DATABASE_URL is set, but psycopg2 is not installed. "
                "Install dependencies from requirements.txt."
            ) from exc

        raw_connection = psycopg2.connect(
            config.DATABASE_URL,
            cursor_factory=DictCursor,
        )
        return PostgresConnection(raw_connection)

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
        if is_postgres():
            conn.executescript(POSTGRES_SCHEMA)
            # Upgrade databases created before passage deduplication was added.
            conn.execute("ALTER TABLE passages ADD COLUMN IF NOT EXISTS content_hash TEXT")
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS passages_content_hash_idx "
                "ON passages(content_hash)"
            )
        else:
            conn.executescript(SQLITE_SCHEMA)
            columns = {
                row[1] for row in conn.execute("PRAGMA table_info(passages)").fetchall()
            }
            if "content_hash" not in columns:
                conn.execute("ALTER TABLE passages ADD COLUMN content_hash TEXT")
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS passages_content_hash_idx "
                "ON passages(content_hash)"
            )

        # Repair section labels produced by older seed/import code. Practice
        # papers query the canonical ampersand spelling exactly.
        conn.execute(
            """
            UPDATE questions SET section = 'Reading & Writing'
            WHERE LOWER(TRIM(section)) IN (
                'reading and writing', 'reading &amp; writing', 'r&w', 'rw'
            ) AND section != 'Reading & Writing'
            """
        )
