from app.database import is_postgres

class PaperBuilderAgent:
    """
    Builds Digital SAT practice modules with strict adherence to official
    College Board content domain distribution. Module 2 difficulty is
    dynamically routed based on Module 1 performance (>= 65% -> Hard path).
    """

    # Official DSAT domain quotas per module
    RW_QUOTAS = {
        "Craft and Structure": 8,
        "Information and Ideas": 7,
        "Standard English Conventions": 7,
        "Expression of Ideas": 5,
    }

    MATH_QUOTAS = {
        "Algebra": 8,
        "Advanced Math": 7,
        "Problem Solving and Data Analysis": 4,
        "Geometry and Trigonometry": 3,
    }

    ACCURACY_THRESHOLD = 0.65

    def _ph(self, value=None):
        """Return parameterized placeholder based on DB type."""
        return "%s" if is_postgres() else "?"
    
    def _join_ph(self, count):
        """Join N placeholders with commas."""
        ph = self._ph()
        return ", ".join([ph] * count)
    
    def _get_difficulty_band(self, difficulty: str) -> list:
        """Map a difficulty routing label to the DB difficulty values."""
        if difficulty == 'easy':
            return ['Easy', 'Medium']
        elif difficulty == 'hard':
            return ['Medium', 'Hard']
        else:  # baseline for Module 1
            return ['Easy', 'Medium', 'Hard']

    def _fetch_by_topic(self, cursor, section: str, topic: str, diff_band: list,
                        count: int, exclude_ids: list) -> list:
        """
        Fetch exactly `count` question IDs for a specific topic and difficulty band.
        Uses LIKE matching to handle minor topic name variants (e.g. hyphenated vs non-hyphenated).
        Falls back to broader difficulty if not enough questions are available.
        """
        ph = self._ph()
        diff_placeholders = self._join_ph(len(diff_band))
        
        # Replace spaces with % to flexibly match hyphens and spaces
        flex_topic = f"%{topic.replace('-', ' ').replace(' ', '%')}%"

        sql = f"""
            SELECT id FROM questions
            WHERE section = {ph}
              AND topic LIKE {ph}
              AND import_status = 'active'
              AND difficulty IN ({diff_placeholders})
        """
        params = [section, flex_topic] + diff_band

        if exclude_ids:
            excl_placeholders = self._join_ph(len(exclude_ids))
            sql += f" AND id NOT IN ({excl_placeholders})"
            params.extend(exclude_ids)

        sql += f" ORDER BY RANDOM() LIMIT {ph}"
        params.append(count)

        rows = cursor.execute(sql, params).fetchall()
        ids = [r['id'] for r in rows]

        # Fallback: if we couldn't fill the quota from the restricted difficulty band,
        # widen to ALL difficulties for the remaining shortfall
        if len(ids) < count:
            shortfall = count - len(ids)
            already_picked = exclude_ids + ids

            fallback_sql = """
                SELECT id FROM questions
                WHERE section = %s
                  AND topic LIKE %s
                  AND import_status = 'active'
            """
            fallback_params = [section, flex_topic]

            if already_picked:
                fb_excl = self._join_ph(len(already_picked))
                fallback_sql += f" AND id NOT IN ({fb_excl})"
                fallback_params.extend(already_picked)

            fallback_sql += f" ORDER BY RANDOM() LIMIT {ph}"
            fallback_params.append(shortfall)

            fallback_rows = cursor.execute(fallback_sql, fallback_params).fetchall()
            ids.extend([r['id'] for r in fallback_rows])

        return ids

    def build_module(self, cursor, section: str, difficulty: str, count: int, exclude_ids: list) -> list:
        """
        Build a module of `count` questions using official domain quotas.
        
        For Module 1 (difficulty='baseline'): pulls from all difficulty levels.
        For Module 2 (difficulty='easy' or 'hard'): restricts to the adaptive band.
        
        The domain distribution remains identical regardless of which path is taken.
        """
        quotas = self.RW_QUOTAS if section == "Reading & Writing" else self.MATH_QUOTAS
        diff_band = self._get_difficulty_band(difficulty)

        selected_ids = []
        for topic, topic_count in quotas.items():
            topic_ids = self._fetch_by_topic(
                cursor, section, topic, diff_band, topic_count,
                exclude_ids + selected_ids
            )
            selected_ids.extend(topic_ids)

        return selected_ids

    def calculate_accuracy(self, cursor, session_id: str, question_ids: list) -> float:
        """Calculate accuracy for a set of question IDs within a session."""
        if not question_ids:
            return 0.0
        ph = self._ph()
        placeholders = self._join_ph(len(question_ids))
        sql = f"SELECT is_correct FROM user_attempts WHERE session_id = {ph} AND question_id IN ({placeholders})"
        params = [session_id] + question_ids
        attempts = cursor.execute(sql, params).fetchall()
        total = len(attempts)
        if total == 0:
            return 0.0
        correct = sum(1 for a in attempts if a['is_correct'] == 1)
        return correct / total
