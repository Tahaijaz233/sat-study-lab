"""Fetch and idempotently ingest the public OpenSAT question bank."""

import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import httpx

# Add project root to path when this file is executed directly.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.agents.normalization import NormalizationAgent
from app.database import get_db


# Ordered fallbacks. Prefer OpenSAT's canonical community endpoint; keep the
# JSONSilo mirror for resilience when that service is temporarily unavailable.
OPENSAT_URLS = [
    "https://pinesat.duckdns.org/api/questions",
    "https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5",
]
# Backwards-friendly alias used by deployment checks.
API_ENDPOINTS = OPENSAT_URLS

SOURCE_ID = "src_opensat"
SOURCE_NAME = "OpenSAT Community Database"
SOURCE_URI = "https://github.com/Anas099X/OpenSAT"
MATH_DOMAINS = {
    "Algebra",
    "Advanced Math",
    "Problem Solving and Data Analysis",
    "Problem-Solving and Data Analysis",
    "Geometry and Trigonometry",
}

normalizer = NormalizationAgent()


def _response_json(url: str, **kwargs):
    """GET JSON with settings suitable for a community-hosted endpoint."""
    response = httpx.get(
        url,
        timeout=45.0,
        follow_redirects=True,
        headers={"User-Agent": "SAT-Study-Lab/1.0"},
        **kwargs,
    )
    response.raise_for_status()
    return response.json()


def _flatten_payload(payload: Any, section_hint: Optional[str] = None) -> List[Dict[str, Any]]:
    """Normalize both supported API envelope formats into item dictionaries."""
    items: List[Dict[str, Any]] = []

    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        payload = payload["data"]

    if isinstance(payload, list):
        for raw in payload:
            if isinstance(raw, dict):
                item = dict(raw)
                if section_hint:
                    item["_section_hint"] = section_hint
                items.append(item)
        return items

    if isinstance(payload, dict):
        section_keys = (
            ("english", "Reading & Writing"),
            ("reading", "Reading & Writing"),
            ("reading_and_writing", "Reading & Writing"),
            ("math", "Math"),
        )
        for key, canonical_section in section_keys:
            raw_items = payload.get(key)
            if not isinstance(raw_items, list):
                continue
            for raw in raw_items:
                if isinstance(raw, dict):
                    item = dict(raw)
                    item["_section_hint"] = canonical_section
                    items.append(item)

    return items


def fetch_question_bank() -> Tuple[List[Dict[str, Any]], str]:
    """Fetch the complete English and Math bank from the first healthy mirror."""
    errors = []
    for url in OPENSAT_URLS:
        try:
            if "pinesat.duckdns.org" in url:
                # The public API defaults to English, so both requests are
                # necessary to retrieve the *full* bank.
                english = _response_json(url, params={"section": "english"})
                math = _response_json(url, params={"section": "math"})
                items = _flatten_payload(english, "Reading & Writing")
                items.extend(_flatten_payload(math, "Math"))
            else:
                items = _flatten_payload(_response_json(url))

            if items:
                return items, url
            errors.append(f"{url}: empty or unsupported response")
        except Exception as exc:
            errors.append(f"{url}: {exc}")

    raise RuntimeError("All OpenSAT endpoints failed: " + "; ".join(errors))


def _coerce_question_data(item: Dict[str, Any]) -> Dict[str, Any]:
    question_data = item.get("question", {})
    if isinstance(question_data, str):
        value = question_data.strip()
        if value.startswith("{"):
            for parser in (json.loads, ast.literal_eval):
                try:
                    parsed = parser(value)
                    if isinstance(parsed, dict):
                        return parsed
                except Exception:
                    continue
        return {"question": value}
    if isinstance(question_data, dict):
        return question_data
    return {}


def _canonical_topic(topic: Any) -> str:
    value = str(topic or "General SAT Concept").strip()
    if value == "Problem-Solving and Data Analysis":
        return "Problem Solving and Data Analysis"
    return value


def _infer_section(item: Dict[str, Any], topic: str) -> str:
    raw_section = item.get("section") or item.get("_section_hint")
    if raw_section:
        return normalizer.normalize_section(str(raw_section))
    return "Math" if topic in MATH_DOMAINS else "Reading & Writing"


def _infer_subtopic(topic: str, item: Dict[str, Any]) -> str:
    supplied = item.get("skill") or item.get("subtopic")
    if supplied:
        return str(supplied).strip()
    defaults = {
        "Algebra": "Linear Equations",
        "Advanced Math": "Equivalent Expressions",
        "Problem Solving and Data Analysis": "Ratios and Rates",
        "Geometry and Trigonometry": "Lines, Angles, and Triangles",
        "Standard English Conventions": "Boundaries and Sentence Structure",
        "Craft and Structure": "Words in Context",
        "Information and Ideas": "Central Ideas and Details",
        "Expression of Ideas": "Transitions",
    }
    return defaults.get(topic, "General SAT Concept")


def _choice_pairs(raw_choices: Any) -> List[Tuple[str, str]]:
    if isinstance(raw_choices, dict):
        return [(str(letter), str(content)) for letter, content in raw_choices.items()]
    if isinstance(raw_choices, list):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return [
            (letters[index], str(content))
            for index, content in enumerate(raw_choices)
            if index < len(letters)
        ]
    return []


def _upsert_source(cursor):
    existing = cursor.execute("SELECT id FROM sources WHERE id = ?", (SOURCE_ID,)).fetchone()
    if existing:
        cursor.execute(
            """
            UPDATE sources
            SET name = ?, uri = ?, source_type = ?, permission_notes = ?
            WHERE id = ?
            """,
            (SOURCE_NAME, SOURCE_URI, "api", "Open source (MIT)", SOURCE_ID),
        )
    else:
        cursor.execute(
            """
            INSERT INTO sources
                (id, name, uri, source_type, permission_notes, question_count)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (SOURCE_ID, SOURCE_NAME, SOURCE_URI, "api", "Open source (MIT)", 0),
        )


def ingest_questions(items: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    """Insert normalized items, preserving hashes so repeated runs are safe."""
    stats = {"inserted": 0, "duplicates": 0, "skipped": 0}

    with get_db() as conn:
        cursor = conn.cursor()
        _upsert_source(cursor)

        for item in items:
            question_data = _coerce_question_data(item)
            prompt = str(
                question_data.get("question")
                or question_data.get("prompt")
                or item.get("prompt")
                or ""
            ).strip()
            if not prompt:
                stats["skipped"] += 1
                continue

            passage_text = str(
                question_data.get("paragraph")
                or question_data.get("passage")
                or item.get("passage")
                or ""
            ).strip()
            if passage_text.lower() == "null":
                passage_text = ""

            content_hash = normalizer.compute_hash(prompt, passage_text)
            if cursor.execute(
                "SELECT id FROM questions WHERE content_hash = ?", (content_hash,)
            ).fetchone():
                stats["duplicates"] += 1
                continue

            topic = _canonical_topic(item.get("domain") or item.get("topic"))
            section = _infer_section(item, topic)
            subtopic = _infer_subtopic(topic, item)
            difficulty = str(item.get("difficulty") or "Medium").strip().capitalize()
            if difficulty not in {"Easy", "Medium", "Hard"}:
                difficulty = "Medium"

            raw_choices = (
                question_data.get("choices")
                or question_data.get("options")
                or item.get("choices")
                or item.get("options")
                or []
            )
            choices = _choice_pairs(raw_choices)
            correct_answer = str(
                question_data.get("correct_answer")
                or question_data.get("correct")
                or item.get("correct_answer")
                or item.get("correct")
                or ""
            ).strip()
            explanation = str(
                question_data.get("explanation")
                or question_data.get("rationale")
                or item.get("explanation")
                or "Explanation provided by the OpenSAT community."
            ).strip()

            passage_id = None
            if passage_text:
                passage_hash = hashlib.sha256(passage_text.encode("utf-8")).hexdigest()
                passage_row = cursor.execute(
                    "SELECT id FROM passages WHERE content_hash = ?", (passage_hash,)
                ).fetchone()
                if passage_row:
                    passage_id = passage_row["id"]
                else:
                    passage_id = f"opensat_p_{passage_hash[:24]}"
                    cursor.execute(
                        """
                        INSERT INTO passages (
                            id, title, content, passage_type, word_count,
                            source_name, source_uri, content_hash
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            passage_id,
                            f"OpenSAT Passage - {topic}",
                            passage_text,
                            f"{section} Passage",
                            len(passage_text.split()),
                            SOURCE_NAME,
                            SOURCE_URI,
                            passage_hash,
                        ),
                    )

            question_id = f"opensat_q_{content_hash[:24]}"
            question_type = "Multiple Choice" if choices else "Student-Produced Response"
            cursor.execute(
                """
                INSERT INTO questions (
                    id, passage_id, section, topic, subtopic, question_type,
                    difficulty, prompt, answer_explanation, correct_answer_value,
                    source_name, source_uri, import_status, license_notes,
                    content_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    question_id,
                    passage_id,
                    section,
                    topic,
                    subtopic,
                    question_type,
                    difficulty,
                    prompt,
                    explanation,
                    correct_answer,
                    SOURCE_NAME,
                    SOURCE_URI,
                    "active",
                    "Open source (MIT)",
                    content_hash,
                ),
            )

            normalized_correct = correct_answer.upper()
            for index, (letter, content) in enumerate(choices):
                normalized_letter = letter.strip().upper()
                is_correct = int(
                    normalized_correct == normalized_letter
                    or correct_answer.strip() == content.strip()
                )
                choice_hash = hashlib.sha256(
                    f"{question_id}:{index}:{normalized_letter}".encode("utf-8")
                ).hexdigest()[:20]
                cursor.execute(
                    """
                    INSERT INTO choices
                        (id, question_id, choice_letter, content, is_correct)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        f"opensat_c_{choice_hash}",
                        question_id,
                        normalized_letter,
                        content,
                        is_correct,
                    ),
                )

            stats["inserted"] += 1

        cursor.execute(
            """
            UPDATE sources
            SET question_count = (
                SELECT COUNT(*) FROM questions WHERE source_name = ?
            )
            WHERE id = ?
            """,
            (SOURCE_NAME, SOURCE_ID),
        )

    return stats


def fetch_and_ingest() -> Dict[str, Any]:
    """Fetch and ingest the full bank; return structured startup-safe stats."""
    print("[OpenSAT] Fetching the public English and Math question bank...")
    try:
        items, endpoint = fetch_question_bank()
        stats: Dict[str, Any] = ingest_questions(items)
        stats.update({"fetched": len(items), "endpoint": endpoint, "errors": 0})
        print(
            "[OpenSAT] Ingestion complete: "
            f"{stats['inserted']} inserted, {stats['duplicates']} duplicates, "
            f"{stats['skipped']} skipped."
        )
        return stats
    except Exception as exc:
        print(f"[OpenSAT] Ingestion skipped: {exc}")
        return {
            "inserted": 0,
            "duplicates": 0,
            "skipped": 0,
            "fetched": 0,
            "errors": 1,
            "error": str(exc),
        }


if __name__ == "__main__":
    from app.database import init_db

    init_db()
    fetch_and_ingest()
