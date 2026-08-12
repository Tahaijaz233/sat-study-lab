import unittest
import re

class IngestionAgent:
    def parse_pdf(self, text):
        questions = []
        # Basic regex to extract questions numbered like "1. What is..."
        pattern = re.compile(r'(\d+)\.\s+(.*?)(?=\n\d+\.|\Z)', re.DOTALL)
        for match in pattern.finditer(text):
            questions.append({"num": match.group(1), "text": match.group(2).strip()})
        return questions

class TestPDFIngestion(unittest.TestCase):
    def test_pdf_parsing_logic(self):
        mock_pdf_text = """
1. What is the value of x?
A) 1
B) 2
2. Identify the main idea.
This passage is about...
"""
        agent = IngestionAgent()
        results = agent.parse_pdf(mock_pdf_text)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['num'], '1')
        self.assertTrue(results[0]['text'].startswith('What is the value'))
        self.assertEqual(results[1]['num'], '2')
        self.assertTrue(results[1]['text'].startswith('Identify the main idea'))

if __name__ == '__main__':
    unittest.main()
