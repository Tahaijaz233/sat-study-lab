import sqlite3
import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA foreign_keys=ON;")
        self.cursor = self.conn.cursor()
        
        # Create schema for 8 standard tables and 2 FTS5 virtual tables
        self.cursor.execute('''
            CREATE TABLE sources (id INTEGER PRIMARY KEY, name TEXT)
        ''')
        self.cursor.execute('''
            CREATE TABLE questions (
                id INTEGER PRIMARY KEY, 
                content TEXT, 
                content_hash TEXT UNIQUE, 
                source_id INTEGER,
                FOREIGN KEY(source_id) REFERENCES sources(id)
            )
        ''')
        self.cursor.execute('CREATE TABLE answers (id INTEGER PRIMARY KEY, q_id INTEGER, is_correct BOOLEAN)')
        self.cursor.execute('CREATE TABLE vocab (id INTEGER PRIMARY KEY, term TEXT, definition TEXT)')
        self.cursor.execute('CREATE TABLE sessions (id INTEGER PRIMARY KEY, timestamp TEXT)')
        self.cursor.execute('CREATE TABLE attempts (id INTEGER PRIMARY KEY, session_id INTEGER)')
        self.cursor.execute('CREATE TABLE bookmarks (id INTEGER PRIMARY KEY, q_id INTEGER)')
        self.cursor.execute('CREATE TABLE analytics (id INTEGER PRIMARY KEY, user_id INTEGER)')
        
        self.cursor.execute('CREATE VIRTUAL TABLE questions_fts USING fts5(content, content="questions", content_rowid="id")')
        self.cursor.execute('CREATE VIRTUAL TABLE vocab_fts USING fts5(term, definition, content="vocab", content_rowid="id")')
        self.conn.commit()

    def test_pragma_settings(self):
        journal_mode = self.cursor.execute("PRAGMA journal_mode;").fetchone()[0]
        self.assertIn(journal_mode.lower(), ['wal', 'memory'])
        
        foreign_keys = self.cursor.execute("PRAGMA foreign_keys;").fetchone()[0]
        self.assertEqual(foreign_keys, 1)

    def test_schema_creation(self):
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [t[0] for t in tables]
        expected_tables = [
            'sources', 'questions', 'answers', 'vocab', 
            'sessions', 'attempts', 'bookmarks', 'analytics',
            'questions_fts', 'questions_fts_data', 'questions_fts_idx', 'questions_fts_docsize', 'questions_fts_config',
            'vocab_fts', 'vocab_fts_data', 'vocab_fts_idx', 'vocab_fts_docsize', 'vocab_fts_config'
        ]
        for t in ['sources', 'questions', 'answers', 'vocab', 'sessions', 'attempts', 'bookmarks', 'analytics']:
            self.assertIn(t, table_names)

    def test_content_hash_unique_constraint(self):
        self.cursor.execute("INSERT INTO questions (content, content_hash) VALUES ('Q1', 'hash1')")
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("INSERT INTO questions (content, content_hash) VALUES ('Q2', 'hash1')")

    def test_fts5_queries(self):
        self.cursor.execute("INSERT INTO questions (id, content, content_hash) VALUES (1, 'algebra equation', 'h1')")
        self.cursor.execute("INSERT INTO questions_fts (rowid, content) VALUES (1, 'algebra equation')")
        self.conn.commit()
        
        results = self.cursor.execute("SELECT * FROM questions_fts WHERE questions_fts MATCH 'algebra'").fetchall()
        self.assertEqual(len(results), 1)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
