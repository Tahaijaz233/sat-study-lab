import os
import tempfile
import unittest

from app.config import config
from app.database import PostgresCursor, get_db, init_db
from scripts import fetch_opensat_data as opensat


class TestOpenSATHelpers(unittest.TestCase):
    def test_duckdns_endpoint_is_preferred(self):
        self.assertIn("pinesat.duckdns.org", opensat.OPENSAT_URLS[0])

    def test_flatten_list_adds_section_hint(self):
        rows = opensat._flatten_payload([{"id": "1"}], "Math")
        self.assertEqual(rows[0]["_section_hint"], "Math")

    def test_flatten_data_envelope(self):
        rows = opensat._flatten_payload({"data": [{"id": "1"}]}, "Reading & Writing")
        self.assertEqual(rows[0]["id"], "1")

    def test_flatten_grouped_payload(self):
        rows = opensat._flatten_payload({"english": [{"id": "e"}], "math": [{"id": "m"}]})
        self.assertEqual(
            {row["_section_hint"] for row in rows},
            {"Reading & Writing", "Math"},
        )

    def test_coerce_question_dict(self):
        value = {"question": {"question": "Prompt"}}
        self.assertEqual(opensat._coerce_question_data(value)["question"], "Prompt")

    def test_coerce_question_json_string(self):
        value = {"question": '{"question": "Prompt"}'}
        self.assertEqual(opensat._coerce_question_data(value)["question"], "Prompt")

    def test_coerce_question_python_literal(self):
        value = {"question": "{'question': 'Prompt'}"}
        self.assertEqual(opensat._coerce_question_data(value)["question"], "Prompt")

    def test_coerce_plain_question_string(self):
        value = {"question": "Prompt"}
        self.assertEqual(opensat._coerce_question_data(value)["question"], "Prompt")

    def test_canonical_topic_repairs_hyphenated_math_domain(self):
        self.assertEqual(
            opensat._canonical_topic("Problem-Solving and Data Analysis"),
            "Problem Solving and Data Analysis",
        )

    def test_infer_section_normalizes_explicit_name(self):
        item = {"section": "Reading and Writing"}
        self.assertEqual(
            opensat._infer_section(item, "Information and Ideas"),
            "Reading & Writing",
        )

    def test_infer_section_from_math_domain(self):
        self.assertEqual(opensat._infer_section({}, "Algebra"), "Math")

    def test_infer_section_defaults_to_reading(self):
        self.assertEqual(
            opensat._infer_section({}, "Craft and Structure"),
            "Reading & Writing",
        )

    def test_infer_subtopic_uses_supplied_skill(self):
        self.assertEqual(
            opensat._infer_subtopic("Algebra", {"skill": "Linear functions"}),
            "Linear functions",
        )

    def test_choice_pairs_accept_mapping(self):
        self.assertEqual(
            opensat._choice_pairs({"A": "One", "B": "Two"}),
            [("A", "One"), ("B", "Two")],
        )

    def test_choice_pairs_letters_a_list(self):
        self.assertEqual(
            opensat._choice_pairs(["One", "Two"]),
            [("A", "One"), ("B", "Two")],
        )


class TestOpenSATIngestion(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = config.DB_PATH
        self.original_database_url = config.DATABASE_URL
        config.DATABASE_URL = ""
        config.DB_PATH = os.path.join(self.temp_dir.name, "test.db")
        init_db()

    def tearDown(self):
        config.DB_PATH = self.original_db_path
        config.DATABASE_URL = self.original_database_url
        self.temp_dir.cleanup()

    @staticmethod
    def sample(section="Reading and Writing", domain="Information and Ideas"):
        return {
            "domain": domain,
            "_section_hint": section,
            "difficulty": "medium",
            "question": {
                "question": f"Sample prompt for {domain}",
                "paragraph": "A sample passage.",
                "choices": {"A": "Yes", "B": "No", "C": "Maybe", "D": "Never"},
                "correct_answer": "A",
                "explanation": "A is correct.",
            },
        }

    def test_ingest_inserts_question_and_choices(self):
        stats = opensat.ingest_questions([self.sample()])
        with get_db() as conn:
            question_count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
            choice_count = conn.execute("SELECT COUNT(*) FROM choices").fetchone()[0]
        self.assertEqual(stats["inserted"], 1)
        self.assertEqual((question_count, choice_count), (1, 4))

    def test_ingest_is_idempotent(self):
        item = self.sample()
        opensat.ingest_questions([item])
        stats = opensat.ingest_questions([item])
        self.assertEqual(stats["duplicates"], 1)

    def test_ingest_updates_source_count(self):
        opensat.ingest_questions([self.sample()])
        with get_db() as conn:
            count = conn.execute(
                "SELECT question_count FROM sources WHERE id = ?", (opensat.SOURCE_ID,)
            ).fetchone()[0]
        self.assertEqual(count, 1)

    def test_ingest_normalizes_reading_section(self):
        opensat.ingest_questions([self.sample()])
        with get_db() as conn:
            section = conn.execute("SELECT section FROM questions").fetchone()[0]
        self.assertEqual(section, "Reading & Writing")

    def test_ingest_math_section(self):
        opensat.ingest_questions([self.sample("math", "Algebra")])
        with get_db() as conn:
            section = conn.execute("SELECT section FROM questions").fetchone()[0]
        self.assertEqual(section, "Math")

    def test_init_repairs_legacy_section_name(self):
        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO questions (
                    id, section, topic, subtopic, question_type, difficulty,
                    prompt, answer_explanation, source_name, content_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "legacy",
                    "Reading and Writing",
                    "Information and Ideas",
                    "Central Ideas and Details",
                    "Multiple Choice",
                    "Medium",
                    "Legacy prompt",
                    "Legacy explanation",
                    "Legacy",
                    "legacy-hash",
                ),
            )
        init_db()
        with get_db() as conn:
            section = conn.execute(
                "SELECT section FROM questions WHERE id = 'legacy'"
            ).fetchone()[0]
        self.assertEqual(section, "Reading & Writing")

    def test_ingest_cleans_passage_trailing_question(self):
        sample = {
            "domain": "Craft and Structure",
            "_section_hint": "Reading & Writing",
            "difficulty": "medium",
            "question": {
                "question": "The author's organization is intended to",
                "paragraph": "A historical text about sports. What is the author's structure?",
                "choices": {"A": "Yes", "B": "No"},
                "correct_answer": "A",
                "explanation": "Correct",
            },
        }
        opensat.ingest_questions([sample])
        with get_db() as conn:
            passage = conn.execute("SELECT content FROM passages").fetchone()[0]
        self.assertEqual(passage, "A historical text about sports.")

    def test_desmos_api_key_configuration(self):
        self.assertTrue(bool(config.DESMOS_API_KEY))


class TestPostgresCompatibility(unittest.TestCase):
    def test_translates_question_mark_parameters(self):
        self.assertEqual(
            PostgresCursor._translate("SELECT * FROM questions WHERE id = ?"),
            "SELECT * FROM questions WHERE id = %s",
        )

    def test_translates_insert_or_ignore(self):
        self.assertEqual(
            PostgresCursor._translate("INSERT OR IGNORE INTO x (id) VALUES (?);"),
            "INSERT INTO x (id) VALUES (%s) ON CONFLICT DO NOTHING;",
        )

    def test_translates_insert_or_replace(self):
        self.assertEqual(
            PostgresCursor._translate("INSERT OR REPLACE INTO x (id) VALUES (?)"),
            "INSERT INTO x (id) VALUES (%s) ON CONFLICT DO NOTHING",
        )

    def test_leaves_portable_sql_unchanged(self):
        sql = "SELECT COUNT(*) FROM questions"
        self.assertEqual(PostgresCursor._translate(sql), sql)


if __name__ == "__main__":
    unittest.main()
