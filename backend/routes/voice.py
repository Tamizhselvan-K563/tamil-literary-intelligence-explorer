import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from faster_whisper import WhisperModel

from database import get_db
from models import Word, Meaning
from utils.normalization import normalize_tamil
from utils.fuzzy import find_best_match


router = APIRouter(
    prefix="/voice",
    tags=["Voice Search"]
)


# Load Whisper model
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


@router.post("/transcribe")
async def transcribe_voice(
    audio: UploadFile = File(...)
):
    if not audio:
        raise HTTPException(
            status_code=400,
            detail="Audio file is required"
        )

    audio_data = await audio.read()

    if not audio_data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded audio file is empty"
        )

    temp_path = None

    try:

        suffix = os.path.splitext(
            audio.filename or ""
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(audio_data)
            temp_path = temp_file.name

        segments, info = model.transcribe(
            temp_path,
            language="ta",
            beam_size=5
        )

        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        )

        normalized_text = normalize_tamil(
            transcript
        )

        return {
            "language": info.language,
            "text": transcript,
            "normalized_text": normalized_text
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Voice transcription failed: {str(e)}"
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/search")
async def voice_search(
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not audio:
        raise HTTPException(
            status_code=400,
            detail="Audio file is required"
        )

    audio_data = await audio.read()

    if not audio_data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded audio file is empty"
        )

    temp_path = None

    try:

        # --------------------------------
        # 1. Save uploaded audio
        # --------------------------------

        suffix = os.path.splitext(
            audio.filename or ""
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(audio_data)
            temp_path = temp_file.name


        # --------------------------------
        # 2. Convert speech → Tamil text
        # --------------------------------

        segments, info = model.transcribe(
            temp_path,
            language="ta",
            beam_size=5
        )

        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        )

        normalized_text = normalize_tamil(
            transcript
        )


        # --------------------------------
        # 3. Try exact database match
        # --------------------------------

        exact_word = (
            db.query(Word)
            .filter(
                Word.normalized_word == normalized_text
            )
            .first()
        )


        if exact_word:

            best_word = exact_word
            match_score = 1.0
            match_type = "exact"


        # --------------------------------
        # 4. If no exact match → fuzzy match
        # --------------------------------

        else:

            words = db.query(Word).all()

            best_word, match_score = find_best_match(
                normalized_text,
                words,
                threshold=0.65
            )

            match_type = "fuzzy"


        # --------------------------------
        # 5. No suitable match
        # --------------------------------

        if not best_word:

            return {
                "language": info.language,
                "transcript": transcript,
                "normalized_text": normalized_text,
                "matched_word": None,
                "match_score": round(match_score, 2),
                "match_type": "none",
                "results": []
            }


        # --------------------------------
        # 6. Get meanings
        # --------------------------------

        meanings = (
            db.query(Meaning)
            .filter(
                Meaning.word_id == best_word.id
            )
            .all()
        )


        results = []

        for meaning in meanings:

            results.append({

                "word": best_word.word,

                "transliteration":
                    best_word.transliteration,

                "meaning_tamil":
                    meaning.meaning_tamil,

                "meaning_english":
                    meaning.meaning_english,

                "score":
                    round(match_score, 2)

            })


        # --------------------------------
        # 7. Return result
        # --------------------------------

        return {

            "language":
                info.language,

            "transcript":
                transcript,

            "normalized_text":
                normalized_text,

            "matched_word":
                best_word.word,

            "match_score":
                round(match_score, 2),

            "match_type":
                match_type,

            "results":
                results
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Voice search failed: {str(e)}"
        )


    finally:

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)