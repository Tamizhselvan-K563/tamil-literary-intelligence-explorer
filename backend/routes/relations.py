from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, aliased

from database import get_db
from models import Word, Relation
from utils.normalization import normalize_tamil


router = APIRouter(
    prefix="/relations",
    tags=["Relations"]
)


@router.get("/{word}")
def get_relations(
    word: str,
    db: Session = Depends(get_db)
):

    # Normalize the user's input
    normalized_input = normalize_tamil(word)

    # Find the word using its normalized form
    source_word = (
        db.query(Word)
        .filter(Word.normalized_word == normalized_input)
        .first()
    )

    # If the word does not exist
    if not source_word:
        raise HTTPException(
            status_code=404,
            detail=f"Word '{word}' not found"
        )

    # Create an alias for the related word
    related_word = aliased(Word)

    # Get all relationships for the word
    results = (
        db.query(
            Relation.relation_type,
            related_word.word.label("related_word"),
            Relation.confidence,
            Relation.source
        )
        .join(
            related_word,
            Relation.related_word_id == related_word.id
        )
        .filter(
            Relation.word_id == source_word.id
        )
        .all()
    )

    # Format the response
    return {
        "word": source_word.word,
        "relations": [
            {
                "relation_type": relation_type,
                "related_word": related_word,
                "confidence": confidence,
                "source": source
            }
            for relation_type, related_word, confidence, source in results
        ]
    }