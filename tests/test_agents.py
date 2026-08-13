import unittest
import hashlib
from app.agents.normalization import NormalizationAgent
from app.agents.paper_builder import PaperBuilderAgent

class QAComplianceAgent:
    def audit(self, data):
        errors = []
        if 'title' not in data:
            errors.append('missing_title')
        if len(set(data.get('hashes', []))) != len(data.get('hashes', [])):
            errors.append('duplicate_hash')
        if 'license' not in data:
            errors.append('missing_license')
        return errors

class TestAgents(unittest.TestCase):
    def test_normalization_agent(self):
        agent = NormalizationAgent()
        h = agent.compute_hash("test")
        self.assertEqual(h, hashlib.sha256(b"test").hexdigest())

        # Test section normalization
        self.assertEqual(agent.normalize_section("Reading and Writing"), "Reading & Writing")
        self.assertEqual(agent.normalize_section("r&w"), "Reading & Writing")
        self.assertEqual(agent.normalize_section("maths"), "Math")
        self.assertEqual(agent.normalize_section("Mathematics"), "Math")

        q_norm = agent.normalize_question({"prompt": "Hello", "section": "Reading and Writing"})
        self.assertEqual(q_norm["section"], "Reading & Writing")
        self.assertIn("content_hash", q_norm)

    def test_normalization_clean_text_and_passage(self):
        agent = NormalizationAgent()
        
        # Test clean_text
        corrupted = "It\ufffdll be \"quoted\" and \\'escaped\\'"
        self.assertEqual(agent.clean_text(corrupted), "It'll be \"quoted\" and 'escaped'")
        
        # Test clean_passage stripping trailing questions
        raw_passage = (
            "The author writes about the history of a particular sport, starting with the earliest known uses of the sport. "
            "What is the most likely reason why the author structures the passage in this way?"
        )
        expected = "The author writes about the history of a particular sport, starting with the earliest known uses of the sport."
        self.assertEqual(agent.clean_passage(raw_passage), expected)
        
        # Test standalone question becomes empty passage
        standalone = "What is the primary purpose of the text?"
        self.assertEqual(agent.clean_passage(standalone), "")

    def test_paper_builder_domain_quotas(self):
        """Test that PaperBuilderAgent has the correct domain quotas defined."""
        agent = PaperBuilderAgent()
        
        # Verify RW quotas sum to 27
        self.assertEqual(sum(agent.RW_QUOTAS.values()), 27)
        self.assertEqual(agent.RW_QUOTAS["Craft and Structure"], 8)
        self.assertEqual(agent.RW_QUOTAS["Information and Ideas"], 7)
        self.assertEqual(agent.RW_QUOTAS["Standard English Conventions"], 7)
        self.assertEqual(agent.RW_QUOTAS["Expression of Ideas"], 5)
        
        # Verify Math quotas sum to 22
        self.assertEqual(sum(agent.MATH_QUOTAS.values()), 22)
        self.assertEqual(agent.MATH_QUOTAS["Algebra"], 8)
        self.assertEqual(agent.MATH_QUOTAS["Advanced Math"], 7)
        self.assertEqual(agent.MATH_QUOTAS["Problem Solving and Data Analysis"], 4)
        self.assertEqual(agent.MATH_QUOTAS["Geometry and Trigonometry"], 3)

    def test_paper_builder_difficulty_bands(self):
        """Test that difficulty bands map correctly."""
        agent = PaperBuilderAgent()
        
        self.assertEqual(agent._get_difficulty_band('baseline'), ['Easy', 'Medium', 'Hard'])
        self.assertEqual(agent._get_difficulty_band('easy'), ['Easy', 'Medium'])
        self.assertEqual(agent._get_difficulty_band('hard'), ['Medium', 'Hard'])

    def test_paper_builder_accuracy(self):
        agent = PaperBuilderAgent()
        
        # Test accuracy calculation with a mock cursor
        class MockCursor:
            def __init__(self, data):
                self.data = data
            def execute(self, sql, params):
                class MockResult:
                    def __init__(self, res):
                        self.res = res
                    def fetchall(self):
                        return self.res
                return MockResult(self.data)
                
        # 3 correct out of 4 = 0.75
        mock_cursor = MockCursor([{'is_correct': 1}, {'is_correct': 1}, {'is_correct': 0}, {'is_correct': 1}])
        acc = agent.calculate_accuracy(mock_cursor, "sess_1", ["q1", "q2", "q3", "q4"])
        self.assertEqual(acc, 0.75)
        
        # 0 out of 0
        acc_empty = agent.calculate_accuracy(mock_cursor, "sess_1", [])
        self.assertEqual(acc_empty, 0.0)
        
        # Accuracy threshold
        self.assertEqual(agent.ACCURACY_THRESHOLD, 0.65)

    def test_qa_compliance_agent(self):
        agent = QAComplianceAgent()
        errors = agent.audit({'hashes': ['a', 'a']})
        self.assertIn('missing_title', errors)
        self.assertIn('duplicate_hash', errors)
        self.assertIn('missing_license', errors)
        
        errors2 = agent.audit({'title': 'T', 'hashes': ['a', 'b'], 'license': 'MIT'})
        self.assertEqual(errors2, [])

if __name__ == '__main__':
    unittest.main()
