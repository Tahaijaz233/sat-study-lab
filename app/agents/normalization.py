import hashlib
from typing import Dict, Any

class NormalizationAgent:
    def compute_hash(self, prompt: str, passage: str = "") -> str:
        return hashlib.sha256((prompt + (passage or "")).encode('utf-8')).hexdigest()

    def normalize_section(self, section: str) -> str:
        if not section:
            return "Reading & Writing"
        sec_clean = str(section).strip().lower()
        if sec_clean in ["reading and writing", "r&w", "reading & writing", "reading", "rw", "reading &amp; writing"]:
            return "Reading & Writing"
        elif sec_clean in ["math", "mathematics", "maths", "m"]:
            return "Math"
        return section

    def normalize_question(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        data = dict(raw_data)
        if "section" in data:
            data["section"] = self.normalize_section(data["section"])
        if "prompt" in data:
            passage = data.get("passage_content") or data.get("passage") or ""
            data["content_hash"] = self.compute_hash(data["prompt"], passage)
        return data
