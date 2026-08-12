import json
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from app.database import get_db, is_postgres
from app.agents.vocab_agent import VocabAgent

router = APIRouter(prefix="/api/vocab", tags=["Vocab"])
vocab_agent = VocabAgent()

class SM2RatingRequest(BaseModel):
    quality: int = Field(ge=0, le=5)

@router.get("")
@router.get("/")
async def list_vocab(
    status: Optional[str] = None,
    q: Optional[str] = None,
    page: int = 1,
    per_page: int = 50
):
    with get_db() as conn:
        cursor = conn.cursor()
        offset = (page - 1) * per_page
        
        where_clauses = []
        params = []
        
        if status and status != 'all':
            where_clauses.append("status = ?")
            params.append(status)
            
        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        
        if q:
            if is_postgres():
                search_clause = """(
                    word ILIKE ? OR definition ILIKE ?
                    OR roots_prefixes_suffixes ILIKE ?
                )"""
                prefix = f"{where_sql} AND" if where_sql else "WHERE"
                sql = f"""
                    SELECT * FROM vocab_terms
                    {prefix} {search_clause}
                    ORDER BY word ASC
                    LIMIT ? OFFSET ?
                """
                params.extend([f"%{q}%"] * 3 + [per_page, offset])
            else:
                prefix = f"{where_sql} AND" if where_sql else "WHERE"
                sql = f"""
                    SELECT v.* FROM vocab_terms v
                    JOIN vocab_fts fts ON v.id = fts.vocab_id
                    {prefix} vocab_fts MATCH ?
                    ORDER BY v.word ASC
                    LIMIT ? OFFSET ?
                """
                params.extend([q, per_page, offset])
        else:
            sql = f"""
                SELECT * FROM vocab_terms
                {where_sql}
                ORDER BY word ASC
                LIMIT ? OFFSET ?
            """
            params.extend([per_page, offset])
            
        rows = cursor.execute(sql, params).fetchall()
        
        def safe_json(val):
            if not val:
                return []
            try:
                res = json.loads(val)
                if isinstance(res, list):
                    return res
                return [res]
            except Exception:
                if isinstance(val, str) and ',' in val:
                    return [s.strip() for s in val.split(',')]
                return [val]

        terms = []
        for r in rows:
            t_dict = dict(r)
            t_dict['synonyms'] = safe_json(r['synonyms'])
            t_dict['antonyms'] = safe_json(r['antonyms'])
            t_dict['usage_examples'] = safe_json(r['usage_examples'])
            t_dict['sentence_completion_drill'] = safe_json(r['sentence_completion_drill'])
            terms.append(t_dict)

        if q and is_postgres():
            count_prefix = f"{where_sql} AND" if where_sql else "WHERE"
            count_sql = f"SELECT COUNT(*) FROM vocab_terms {count_prefix} {search_clause}"
            count_params = params[:len(where_clauses)] + [f"%{q}%"] * 3
        elif q:
            count_prefix = f"{where_sql} AND" if where_sql else "WHERE"
            count_sql = f"""
                SELECT COUNT(*) FROM vocab_terms v
                JOIN vocab_fts fts ON v.id = fts.vocab_id
                {count_prefix} vocab_fts MATCH ?
            """
            count_params = params[:len(where_clauses)] + [q]
        else:
            count_sql = f"SELECT COUNT(*) FROM vocab_terms {where_sql}"
            count_params = params[:len(where_clauses)]
        total_count = cursor.execute(count_sql, count_params).fetchone()[0]

    return {
        "terms": terms,
        "total": total_count,
        "page": page,
        "per_page": per_page
    }

@router.post("/{vocab_id}/rate")
async def rate_vocab_term(vocab_id: str, req: SM2RatingRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM vocab_terms WHERE id = ?", (vocab_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Vocab term not found")
            
        reps, interval, ef, status = vocab_agent.apply_sm2(
            q=req.quality,
            repetitions=row['repetition_count'],
            interval=row['repetition_interval'],
            ef=row['repetition_efactor']
        )
        
        cursor.execute("""
            UPDATE vocab_terms
            SET repetition_count = ?, repetition_interval = ?, repetition_efactor = ?, status = ?
            WHERE id = ?
        """, (reps, interval, ef, status, vocab_id))

    return {
        "vocab_id": vocab_id,
        "quality": req.quality,
        "new_repetitions": reps,
        "new_interval": interval,
        "new_ef": ef,
        "new_status": status
    }
