import re
import httpx
from typing import List, Dict, Any

class DatasetAuditorAgent:
    def evaluate_sample(self, dataset_name: str, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates a list of questions (sample size N) across 5 metrics:
        1. Schema & Options Completeness (30 pts)
        2. Math & LaTeX Integrity (25 pts)
        3. Passage Integration (20 pts)
        4. Explanations & Rationale (15 pts)
        5. Text Cleanliness (10 pts)
        """
        total = len(questions)
        if total == 0:
            return {
                "dataset_name": dataset_name,
                "sample_size": 0,
                "overall_score": 0,
                "completeness_score": "0 / 30",
                "latex_score": "0 / 25",
                "passage_score": "0 / 20",
                "explanation_score": "0 / 15",
                "cleanliness_score": "0 / 10"
            }

        completeness_pts = 0
        latex_pts = 0
        passage_pts = 0
        explanation_pts = 0
        cleanliness_pts = 0

        for q in questions:
            prompt = q.get('prompt') or q.get('question') or q.get('passage_and_question') or ''
            choices = q.get('choices') or q.get('options') or []
            correct = q.get('correct_answer_value') or q.get('answer') or q.get('label') or ''
            explanation = q.get('answer_explanation') or q.get('explanation') or q.get('rationale') or ''
            passage = q.get('passage') or q.get('passage_content') or ''
            
            # 1. Completeness (30 pts)
            has_prompt = bool(str(prompt).strip())
            has_answer = bool(str(correct).strip())
            has_choices = len(choices) >= 4 or bool(q.get('question_type') == 'Student-Produced Response')
            
            comp_sub = 0
            if has_prompt: comp_sub += 10
            if has_answer: comp_sub += 10
            if has_choices: comp_sub += 10
            completeness_pts += comp_sub

            # 2. Math & LaTeX Integrity (25 pts)
            text_block = str(prompt) + ' ' + ' '.join([str(c) for c in choices])
            dollars = text_block.count('$')
            math_valid = True
            if dollars % 2 != 0:
                math_valid = False
            if r'\frac' in text_block and '$' not in text_block and r'\(' not in text_block:
                math_valid = False
                
            if math_valid:
                latex_pts += 25
            else:
                latex_pts += 10

            # 3. Passage Integration (20 pts)
            is_rw = 'reading' in str(q.get('section', '')).lower() or 'english' in str(q.get('section', '')).lower() or len(str(prompt)) > 150
            if is_rw:
                if passage or (len(str(prompt)) > 200 and '\n' in str(prompt)):
                    passage_pts += 20
                else:
                    passage_pts += 5
            else:
                passage_pts += 20

            # 4. Explanations (15 pts)
            if explanation and len(str(explanation).strip()) > 20:
                explanation_pts += 15
            elif explanation:
                explanation_pts += 8

            # 5. Cleanliness (10 pts)
            clean_sub = 10
            if r'\u20' in text_block or r'\u00' in text_block:
                clean_sub -= 4
            if '<div' in text_block or '<p>' in text_block:
                clean_sub -= 3
            cleanliness_pts += max(0, clean_sub)

        avg_completeness = round(completeness_pts / total, 1)
        avg_latex = round(latex_pts / total, 1)
        avg_passage = round(passage_pts / total, 1)
        avg_explanation = round(explanation_pts / total, 1)
        avg_cleanliness = round(cleanliness_pts / total, 1)
        
        overall = round(avg_completeness + avg_latex + avg_passage + avg_explanation + avg_cleanliness, 1)

        return {
            "dataset_name": dataset_name,
            "sample_size": total,
            "overall_score": overall,
            "completeness_score": f"{avg_completeness} / 30",
            "latex_score": f"{avg_latex} / 25",
            "passage_score": f"{avg_passage} / 20",
            "explanation_score": f"{avg_explanation} / 15",
            "cleanliness_score": f"{avg_cleanliness} / 10"
        }
