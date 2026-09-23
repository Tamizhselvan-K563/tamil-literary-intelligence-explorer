from pydantic import BaseModel
from typing import Optional


class MeaningResponse(BaseModel):
    id: int
    meaning_tamil: str
    meaning_english: Optional[str] = None
    source: Optional[str] = None


class WordResponse(BaseModel):
    id: int
    word: str
    normalized_word: str
    transliteration: Optional[str] = None
    part_of_speech: Optional[str] = None
    source: Optional[str] = None
    meanings: list[MeaningResponse] = []