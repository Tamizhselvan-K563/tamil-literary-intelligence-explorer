from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, aliased

from database import get_db
from models import Word, Relation
from utils.normalization import normalize_tamil


router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)


@router.get("/{word}")
def get_graph(
    word: str,
    db: Session = Depends(get_db)
):

    # Normalize the user's input
    normalized_input = normalize_tamil(word)

    # Find the main word using its normalized form
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

    # Get all relationships connected to the main word
    results = (
        db.query(
            Relation.relation_type,
            related_word.id.label("related_id"),
            related_word.word.label("related_word")
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

    # Create the main node
    nodes = [
        {
            "id": source_word.id,
            "label": source_word.word,
            "type": "main"
        }
    ]

    # Create relationship edges
    edges = []

    for relation_type, related_id, related_word_name in results:

        nodes.append(
            {
                "id": related_id,
                "label": related_word_name,
                "type": "related"
            }
        )

        edges.append(
            {
                "source": source_word.id,
                "target": related_id,
                "relation": relation_type
            }
        )

    # Return graph data
    return {
        "word": source_word.word,
        "nodes": nodes,
        "edges": edges
    }