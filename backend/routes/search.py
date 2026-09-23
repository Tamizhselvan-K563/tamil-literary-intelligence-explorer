from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Word, Meaning
from utils.normalization import normalize_tamil


router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.post("")
def semantic_search(
    query: str,
    db: Session = Depends(get_db)
):

    # Normalize the user's search query
    normalized_query = normalize_tamil(query)

    # Get all words and their meanings
    results = (
        db.query(Word, Meaning)
        .join(
            Meaning,
            Meaning.word_id == Word.id
        )
        .all()
    )

    matches = []

    for word, meaning in results:

        # Normalize database values
        word_text = normalize_tamil(word.word)
        tamil_meaning = normalize_tamil(meaning.meaning_tamil)

        english_meaning = (
            meaning.meaning_english.lower().strip()
            if meaning.meaning_english
            else ""
        )

        # Search in word, Tamil meaning, or English meaning
        if (
            normalized_query in word_text
            or normalized_query in tamil_meaning
            or normalized_query.lower() in english_meaning
        ):

            matches.append(
                {
                    "word": word.word,
                    "transliteration": word.transliteration,
                    "meaning_tamil": meaning.meaning_tamil,
                    "meaning_english": meaning.meaning_english,
                    "score": 1.0
                }
            )

    return {
        "query": query,
        "normalized_query": normalized_query,
        "results": matches
    }