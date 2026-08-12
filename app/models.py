from pydantic import BaseModel
from typing import List, Optional

class ChoiceCreate(BaseModel):
    content: str
    is_correct: bool

class QuestionCreate(BaseModel):
    passage_id: Optional[int] = None
    prompt: str
    choices: List[ChoiceCreate]
    tags: List[str] = []

class QuestionResponse(BaseModel):
    id: int
    prompt: str
    passage_id: Optional[int] = None
    content_hash: str

class VocabTermCreate(BaseModel):
    term: str
    definition: str

class SM2Rating(BaseModel):
    q: int

class PracticeSessionCreate(BaseModel):
    num_rw: int = 27
    num_math: int = 22

class AttemptSubmit(BaseModel):
    question_id: int
    choice_id: int

class SourceResponse(BaseModel):
    id: int
    name: str
    license_note: str
