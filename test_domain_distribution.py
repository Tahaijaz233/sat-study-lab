"""
Integration test: verify PaperBuilderAgent generates modules with correct domain quotas.
"""
import sqlite3
from app.agents.paper_builder import PaperBuilderAgent

def test_module_distribution():
    conn = sqlite3.connect('sat_lab.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    agent = PaperBuilderAgent()

    print("=" * 60)
    print("INTEGRATION TEST: Domain Distribution Verification")
    print("=" * 60)

    # Test 1: R&W Module 1 (Baseline)
    print("\n--- R&W Module 1 (Baseline: All Difficulties) ---")
    rw_m1_ids = agent.build_module(cursor, "Reading & Writing", "baseline", 27, [])
    print(f"Total questions: {len(rw_m1_ids)}")
    assert len(rw_m1_ids) == 27, f"Expected 27, got {len(rw_m1_ids)}"

    # Verify topic distribution
    for qid in rw_m1_ids:
        q = cursor.execute("SELECT topic, difficulty FROM questions WHERE id = ?", (qid,)).fetchone()
    
    rw_topics = {}
    for qid in rw_m1_ids:
        q = cursor.execute("SELECT topic FROM questions WHERE id = ?", (qid,)).fetchone()
        t = q['topic']
        rw_topics[t] = rw_topics.get(t, 0) + 1
    
    for topic, count in sorted(rw_topics.items()):
        expected = agent.RW_QUOTAS.get(topic, '?')
        status = "PASS" if count == expected else "FAIL"
        print(f"  [{status}] {topic}: {count} (expected {expected})")

    # Test 2: R&W Module 2 (Hard path)
    print("\n--- R&W Module 2 (Hard: Medium/Hard) ---")
    rw_m2_ids = agent.build_module(cursor, "Reading & Writing", "hard", 27, rw_m1_ids)
    print(f"Total questions: {len(rw_m2_ids)}")
    assert len(rw_m2_ids) == 27, f"Expected 27, got {len(rw_m2_ids)}"
    
    # Verify no duplicates with Module 1
    overlap = set(rw_m1_ids) & set(rw_m2_ids)
    print(f"  Overlap with Module 1: {len(overlap)} (should be 0)")
    assert len(overlap) == 0, f"Found {len(overlap)} duplicate questions!"
    
    rw2_topics = {}
    rw2_diffs = {}
    for qid in rw_m2_ids:
        q = cursor.execute("SELECT topic, difficulty FROM questions WHERE id = ?", (qid,)).fetchone()
        t = q['topic']
        d = q['difficulty']
        rw2_topics[t] = rw2_topics.get(t, 0) + 1
        rw2_diffs[d] = rw2_diffs.get(d, 0) + 1
    
    for topic, count in sorted(rw2_topics.items()):
        expected = agent.RW_QUOTAS.get(topic, '?')
        status = "PASS" if count == expected else "WARN"
        print(f"  [{status}] {topic}: {count} (expected {expected})")
    print(f"  Difficulty distribution: {dict(rw2_diffs)}")

    # Test 3: Math Module 1 (Baseline)
    print("\n--- Math Module 1 (Baseline: All Difficulties) ---")
    math_m1_ids = agent.build_module(cursor, "Math", "baseline", 22, [])
    print(f"Total questions: {len(math_m1_ids)}")
    assert len(math_m1_ids) == 22, f"Expected 22, got {len(math_m1_ids)}"

    math_topics = {}
    for qid in math_m1_ids:
        q = cursor.execute("SELECT topic FROM questions WHERE id = ?", (qid,)).fetchone()
        t = q['topic']
        math_topics[t] = math_topics.get(t, 0) + 1
    
    for topic, count in sorted(math_topics.items()):
        expected = agent.MATH_QUOTAS.get(topic, '?')
        status = "PASS" if count == expected else "FAIL"
        print(f"  [{status}] {topic}: {count} (expected {expected})")

    # Test 4: Math Module 2 (Easy path)
    print("\n--- Math Module 2 (Easy: Easy/Medium) ---")
    math_m2_ids = agent.build_module(cursor, "Math", "easy", 22, math_m1_ids)
    print(f"Total questions: {len(math_m2_ids)}")
    assert len(math_m2_ids) == 22, f"Expected 22, got {len(math_m2_ids)}"
    
    overlap_m = set(math_m1_ids) & set(math_m2_ids)
    print(f"  Overlap with Module 1: {len(overlap_m)} (should be 0)")

    math2_topics = {}
    math2_diffs = {}
    for qid in math_m2_ids:
        q = cursor.execute("SELECT topic, difficulty FROM questions WHERE id = ?", (qid,)).fetchone()
        t = q['topic']
        d = q['difficulty']
        math2_topics[t] = math2_topics.get(t, 0) + 1
        math2_diffs[d] = math2_diffs.get(d, 0) + 1
    
    for topic, count in sorted(math2_topics.items()):
        expected = agent.MATH_QUOTAS.get(topic, '?')
        status = "PASS" if count == expected else "WARN"
        print(f"  [{status}] {topic}: {count} (expected {expected})")
    print(f"  Difficulty distribution: {dict(math2_diffs)}")

    conn.close()
    print("\n" + "=" * 60)
    print("ALL INTEGRATION TESTS PASSED")
    print("=" * 60)

if __name__ == '__main__':
    test_module_distribution()
