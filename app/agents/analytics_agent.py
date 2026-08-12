import sqlite3
from typing import Dict, List, Any

class AnalyticsAgent:
    def estimate_section_score(self, accuracy: float) -> int:
        if accuracy <= 0:
            return 200
        if accuracy >= 1.0:
            return 800
        if accuracy < 0.5:
            return int(200 + accuracy * 500)
        elif accuracy < 0.75:
            return int(450 + (accuracy - 0.5) * 600)
        else:
            return int(600 + (accuracy - 0.75) * 800)

    def compute_dashboard_stats(self, conn: sqlite3.Connection) -> Dict[str, Any]:
        cursor = conn.cursor()
        
        # Completed sessions count
        sessions_row = cursor.execute("SELECT COUNT(*) FROM practice_sessions WHERE status = 'completed'").fetchone()
        completed_sessions = sessions_row[0] if sessions_row else 0
        
        # Attempts stats
        attempts_row = cursor.execute("""
            SELECT 
                COUNT(*) as total_attempts,
                COALESCE(SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END), 0) as correct_attempts
            FROM user_attempts
        """).fetchone()
        
        total_attempts = attempts_row['total_attempts'] if attempts_row else 0
        correct_attempts = attempts_row['correct_attempts'] if attempts_row else 0
        
        overall_accuracy = round((correct_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0.0
        
        # Section breakdowns
        rw_attempts_row = cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COALESCE(SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END), 0) as correct
            FROM user_attempts ua
            JOIN questions q ON ua.question_id = q.id
            WHERE q.section = 'Reading and Writing'
        """).fetchone()
        
        rw_total = rw_attempts_row['total'] if rw_attempts_row else 0
        rw_correct = rw_attempts_row['correct'] if rw_attempts_row else 0
        rw_acc = (rw_correct / rw_total) if rw_total > 0 else 0.0
        rw_score = self.estimate_section_score(rw_acc) if rw_total > 0 else 0
        
        math_attempts_row = cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COALESCE(SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END), 0) as correct
            FROM user_attempts ua
            JOIN questions q ON ua.question_id = q.id
            WHERE q.section = 'Math'
        """).fetchone()
        
        math_total = math_attempts_row['total'] if math_attempts_row else 0
        math_correct = math_attempts_row['correct'] if math_attempts_row else 0
        math_acc = (math_correct / math_total) if math_total > 0 else 0.0
        math_score = self.estimate_section_score(math_acc) if math_total > 0 else 0
        
        total_estimated_score = (rw_score + math_score) if (rw_total > 0 or math_total > 0) else 0

        # Due vocab terms count
        vocab_due_row = cursor.execute("""
            SELECT COUNT(*) FROM vocab_terms 
            WHERE status IN ('unseen', 'forgotten', 'shaky')
        """).fetchone()
        vocab_due = vocab_due_row[0] if vocab_due_row else 0

        # Recent sessions / activity
        recent_sessions_rows = cursor.execute("""
            SELECT id, title, section, score_scaled, status, created_at 
            FROM practice_sessions 
            ORDER BY created_at DESC 
            LIMIT 5
        """).fetchall()
        
        recent_activity = [dict(row) for row in recent_sessions_rows]

        return {
            "total_questions_attempted": total_attempts,
            "correct_questions_count": correct_attempts,
            "overall_accuracy_percent": overall_accuracy,
            "completed_sessions_count": completed_sessions,
            "estimated_total_score": total_estimated_score,
            "rw_score": rw_score,
            "math_score": math_score,
            "rw_attempts": rw_total,
            "math_attempts": math_total,
            "vocab_due_count": vocab_due,
            "recent_activity": recent_activity
        }

    def get_weak_topics(self, conn: sqlite3.Connection) -> List[Dict[str, Any]]:
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT 
                q.section,
                q.topic,
                COUNT(*) as total_attempts,
                SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END) as correct_attempts
            FROM user_attempts ua
            JOIN questions q ON ua.question_id = q.id
            GROUP BY q.section, q.topic
            HAVING (CAST(correct_attempts AS FLOAT) / total_attempts) < 0.70
        """).fetchall()
        
        weak_areas = []
        for r in rows:
            acc = round((r['correct_attempts'] / r['total_attempts']) * 100, 1)
            weak_areas.append({
                "section": r['section'],
                "topic": r['topic'],
                "total_attempts": r['total_attempts'],
                "correct_attempts": r['correct_attempts'],
                "accuracy_percent": acc
            })
        return weak_areas
