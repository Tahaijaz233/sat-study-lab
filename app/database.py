import os
import re
from contextlib import contextmanager
from app.config import config

# Detect database type from DATABASE_URL
def is_postgres():
    return config.DATABASE_URL.startswith("postgresql://") or config.DATABASE_URL.startswith("postgres://")

def parse_postgres_url(url):
    """Parse postgresql:// URL into connection parameters."""
    pattern = r"postgresql://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/(.+)"
    match = re.match(pattern, url)
    if match:
        return {
            "user": match.group(1),
            "password": match.group(2),
            "host": match.group(3),
            "port": match.group(4) or "5432",
            "dbname": match.group(5)
        }
    return None

# -----------------------------------------------------------------------------
# PostgreSQL Connection (using psycopg2)
# -----------------------------------------------------------------------------

try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

def get_postgres_connection():
    """Get a PostgreSQL connection using psycopg2."""
    if not PSYCOPG2_AVAILABLE:
        raise ImportError("psycopg2 is required for PostgreSQL. Install with: pip install psycopg2-binary")
    
    params = parse_postgres_url(config.DATABASE_URL)
    if not params:
        raise ValueError(f"Invalid PostgreSQL URL: {config.DATABASE_URL}")
    
    conn = psycopg2.connect(
        host=params["host"],
        port=params["port"],
        database=params["dbname"],
        user=params["user"],
        password=params["password"]
    )
    conn.autocommit = False
    return PostgresConnectionWrapper(conn)

class PostgresConnectionWrapper:
    """Wrapper providing dict-like cursor interface similar to sqlite3.Row."""
    
    def __init__(self, conn):
        self.conn = conn
        self._row_factory = psycopg2.extras.RealDictCursor
    
    def cursor(self):
        return self.conn.cursor(cursor_factory=self._row_factory)
    
    def execute(self, sql, params=None):
        cur = self.cursor()
        cur.execute(sql, params or [])
        return cur
    
    def executescript(self, sql_script):
        """Execute multiple SQL statements (semicolon-separated)."""
        statements = []
        current = []
        in_string = False
        string_char = None
        
        for char in sql_script:
            if in_string:
                current.append(char)
                if char == string_char:
                    in_string = False
            else:
                if char in ("'", '"'):
                    in_string = True
                    string_char = char
                elif char == ';':
                    stmt = ''.join(current).strip()
                    if stmt:
                        statements.append(stmt)
                    current = []
                else:
                    current.append(char)
        
        if current:
            stmt = ''.join(current).strip()
            if stmt:
                statements.append(stmt)
        
        for stmt in statements:
            if stmt:
                self.execute(stmt)
    
    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()
    
    def close(self):
        self.conn.close()

# -----------------------------------------------------------------------------
# SQLite Connection
# -----------------------------------------------------------------------------

import sqlite3

def get_sqlite_connection():
    """Get a SQLite connection."""
    conn = sqlite3.connect(config.DATABASE_URL.replace("sqlite:///", ""), check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------------------------------------------------------
# Unified Connection Factory
# -----------------------------------------------------------------------------

def get_connection():
    """Get a database connection (PostgreSQL or SQLite based on config)."""
    if is_postgres():
        if not PSYCOPG2_AVAILABLE:
            raise ImportError("psycopg2 is required for PostgreSQL. Install with: pip install psycopg2-binary")
        return get_postgres_connection()
    else:
        return get_sqlite_connection()

@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# -----------------------------------------------------------------------------
# Schema Creation
# -----------------------------------------------------------------------------

def init_db():
    """Initialize the database schema."""
    with get_db() as conn:
        if is_postgres():
            _init_postgres_schema(conn)
        else:
            _init_sqlite_schema(conn)

def _init_sqlite_schema(conn):
    """Create schema for SQLite."""
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

def _init_postgres_schema(conn):
    """Create schema for PostgreSQL with native full-text search."""
    sql = '''
    -- Enable UUID extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- Create tables
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
        id SERIAL PRIMARY KEY,
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
        id SERIAL PRIMARY KEY,
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

    -- Add tsvector columns for full-text search
    ALTER TABLE questions ADD COLUMN IF NOT EXISTS search_vector tsvector;
    ALTER TABLE vocab_terms ADD COLUMN IF NOT EXISTS vocab_search_vector tsvector;

    -- Create GIN indexes
    CREATE INDEX IF NOT EXISTS questions_search_idx ON questions USING GIN(search_vector);
    CREATE INDEX IF NOT EXISTS vocab_search_idx ON vocab_terms USING GIN(vocab_search_vector);

    -- Create trigger function for questions
    CREATE OR REPLACE FUNCTION update_questions_search_vector() RETURNS trigger AS $$
    BEGIN
        NEW.search_vector := to_tsvector('english',
            COALESCE(NEW.prompt, '') || ' ' ||
            COALESCE(NEW.answer_explanation, '') || ' ' ||
            COALESCE(NEW.topic, '') || ' ' ||
            COALESCE(NEW.subtopic, '')
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Create trigger for questions
    DROP TRIGGER IF EXISTS questions_search_update ON questions;
    CREATE TRIGGER questions_search_update
        BEFORE INSERT OR UPDATE ON questions
        FOR EACH ROW
        EXECUTE FUNCTION update_questions_search_vector();

    -- Initialize existing rows
    UPDATE questions SET search_vector = to_tsvector('english',
        COALESCE(prompt, '') || ' ' ||
        COALESCE(answer_explanation, '') || ' ' ||
        COALESCE(topic, '') || ' ' ||
        COALESCE(subtopic, '')
    ) WHERE search_vector IS NULL;

    -- Create trigger function for vocab
    CREATE OR REPLACE FUNCTION update_vocab_search_vector() RETURNS trigger AS $$
    BEGIN
        NEW.vocab_search_vector := to_tsvector('english',
            COALESCE(NEW.word, '') || ' ' ||
            COALESCE(NEW.definition, '') || ' ' ||
            COALESCE(NEW.roots_prefixes_suffixes, '')
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    -- Create trigger for vocab
    DROP TRIGGER IF EXISTS vocab_search_update ON vocab_terms;
    CREATE TRIGGER vocab_search_update
        BEFORE INSERT OR UPDATE ON vocab_terms
        FOR EACH ROW
        EXECUTE FUNCTION update_vocab_search_vector();

    -- Initialize existing vocab rows
    UPDATE vocab_terms SET vocab_search_vector = to_tsvector('english',
        COALESCE(word, '') || ' ' ||
        COALESCE(definition, '') || ' ' ||
        COALESCE(roots_prefixes_suffixes, '')
    ) WHERE vocab_search_vector IS NULL;
    '''
    
    conn.executescript(sql)
