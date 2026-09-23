from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Word
from schemas import WordResponse
from utils.normalization import normalize_tamil


router = APIRouter(
    prefix="/word",
    tags=["Words"]
)


@router.get("/{word}", response_model=WordResponse)
def get_word(word: str, db: Session = Depends(get_db)):

    # Normalize the user's input
    normalized_input = normalize_tamil(word)

    # Search using the normalized word
    result = (
        db.query(Word)
        .filter(Word.normalized_word == normalized_input)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Word '{word}' not found"
        )

    return result