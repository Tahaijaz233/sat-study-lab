import hashlib
import re
from typing import Dict, Any

class NormalizationAgent:
    @staticmethod
    def clean_text(text: Any) -> str:
        if text is None:
            return ""
        text = str(text)
        text = text.replace('\ufffd', "'").replace('\u2018', "'").replace('\u2019', "'")
        text = text.replace('\u201c', '"').replace('\u201d', '"')
        text = text.replace('\u2014', '—').replace('\u2013', '–')
        text = text.replace('\\"', '"').replace("\\'", "'")
        return text.strip()

    @classmethod
    def clean_passage(cls, content: Any) -> str:
        content = cls.clean_text(content)
        if not content or content.lower() == 'null':
            return ""

        cleaned = content
        while cleaned.endswith('?'):
            # Pattern 1: Typical question starter after sentence ending, quotes, braces, or newline
            m = re.search(
                r'([.!]["\']?|\n|\}|["])\s*(What\b|Which\b|Why\b|How\b|In\s+(?:this|the)\s+passage\b|As\s+used\b|According\b|Where\b|Who\b|Whose\b|Whom\b|The\s+(?:author|writer|narrator|text|passage|use|repetition|shift|contrast|phrase|sentence)\b).*\?\s*$',
                cleaned,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if m:
                cleaned = cleaned[:m.start(1) + len(m.group(1))].strip()
                continue

            # Pattern 2: Generic trailing question after punctuation
            m = re.search(r'([.!?]["\']?)\s+([^.!?\n]*\?)\s*$', cleaned)
            if m:
                cleaned = cleaned[:m.start(1) + len(m.group(1))].strip()
                continue

            break

        # If the entire remaining string still ends in '?' and has no declarative sentences before it,
        # then it's a standalone question, not a reading passage.
        if cleaned.endswith('?') and not re.search(r'[.!"\']\s+', cleaned):
            return ""

        return cleaned

    def compute_hash(self, prompt: str, passage: str = "") -> str:
        clean_p = self.clean_text(prompt)
        clean_pass = self.clean_passage(passage)
        return hashlib.sha256((clean_p + (clean_pass or "")).encode('utf-8')).hexdigest()

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
            data["prompt"] = self.clean_text(data["prompt"])
            raw_passage = data.get("passage_content") or data.get("passage") or ""
            cleaned_passage = self.clean_passage(raw_passage)
            if "passage_content" in data:
                data["passage_content"] = cleaned_passage
            data["content_hash"] = self.compute_hash(data["prompt"], cleaned_passage)
        return data
