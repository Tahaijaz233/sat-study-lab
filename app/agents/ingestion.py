import json
from pypdf import PdfReader
import httpx
from scripts.fetch_opensat_data import fetch_and_ingest

class IngestionAgent:
    def from_json(self, json_data):
        return json.loads(json_data)
        
    def from_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
        
    def from_http(self, url):
        return httpx.get(url).text

    def from_opensat_api(self):
        """Fetch and ingest OpenSAT dataset programmatically."""
        return fetch_and_ingest()
