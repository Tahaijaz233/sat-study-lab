import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_pages_routes(self):
        for route in ['/', '/papers', '/bank', '/vocab', '/analytics', '/sources']:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed with status {res.status_code}")
            self.assertIn("text/html", res.headers.get("content-type", ""))

    def test_questions_api(self):
        res = self.client.get('/api/questions')
        self.assertIn(res.status_code, [200, 404])

    def test_vocab_api(self):
        res = self.client.get('/api/vocab')
        self.assertIn(res.status_code, [200, 404])

    def test_analytics_api(self):
        res = self.client.get('/api/analytics')
        self.assertIn(res.status_code, [200, 404])

    def test_sources_api(self):
        res = self.client.get('/api/sources')
        self.assertIn(res.status_code, [200, 404])

if __name__ == '__main__':
    unittest.main()
