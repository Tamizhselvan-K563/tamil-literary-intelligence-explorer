from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Word, LiteraryWork, LiteraryPassage, WordOccurrence
from utils.normalization import normalize_tamil


router = APIRouter(
    prefix="/literature",
    tags=["Literature"]
)


@router.get("/{word}")
def get_literature(
    word: str,
    db: Session = Depends(get_db)
):

    # Normalize the user's input
    normalized_input = normalize_tamil(word)

    # Find the word using its normalized form
    word_record = (
        db.query(Word)
        .filter(Word.normalized_word == normalized_input)
        .first()
    )

    # If the word does not exist
    if not word_record:
        raise HTTPException(
            status_code=404,
            detail=f"Word '{word}' not found"
        )

    # Find literary passages containing the word
    results = (
        db.query(
            LiteraryWork.title,
            LiteraryWork.author,
            LiteraryWork.period,
            LiteraryWork.genre,
            LiteraryPassage.chapter,
            LiteraryPassage.passage
        )
        .join(
            LiteraryPassage,
            LiteraryPassage.work_id == LiteraryWork.id
        )
        .join(
            WordOccurrence,
            WordOccurrence.passage_id == LiteraryPassage.id
        )
        .filter(
            WordOccurrence.word_id == word_record.id
        )
        .all()
    )

    # Return the literary references
    return {
        "word": word_record.word,
        "literature": [
            {
                "title": title,
                "author": author,
                "period": period,
                "genre": genre,
                "chapter": chapter,
                "passage": passage
            }
            for title, author, period, genre, chapter, passage in results
        ]
    }