from database import SessionLocal
from models import (
    Word,
    Meaning,
    Relation,
    LiteraryWork,
    LiteraryPassage,
    WordOccurrence
)


# ============================================================
# WORD DATA
# ============================================================

words_data = [
    {
        "word": "அன்பு",
        "normalized_word": "அன்பு",
        "transliteration": "Anbu",
        "part_of_speech": "Noun",
        "meaning_tamil": "பாசம், நேசம், அக்கறை",
        "meaning_english": "Love, affection, care",
    },
    {
        "word": "பாசம்",
        "normalized_word": "பாசம்",
        "transliteration": "Paasam",
        "part_of_speech": "Noun",
        "meaning_tamil": "அன்பு, நேசம்",
        "meaning_english": "Affection, love",
    },
    {
        "word": "நேசம்",
        "normalized_word": "நேசம்",
        "transliteration": "Nesam",
        "part_of_speech": "Noun",
        "meaning_tamil": "அன்பு, பாசம்",
        "meaning_english": "Love, affection",
    },
    {
        "word": "நட்பு",
        "normalized_word": "நட்பு",
        "transliteration": "Natpu",
        "part_of_speech": "Noun",
        "meaning_tamil": "நண்பர்களுக்கு இடையிலான உறவு",
        "meaning_english": "Friendship",
    },
    {
        "word": "வெறுப்பு",
        "normalized_word": "வெறுப்பு",
        "transliteration": "Veruppu",
        "part_of_speech": "Noun",
        "meaning_tamil": "பகைமை, விருப்பமின்மை",
        "meaning_english": "Hatred, dislike",
    },
    {
        "word": "அறம்",
        "normalized_word": "அறம்",
        "transliteration": "Aram",
        "part_of_speech": "Noun",
        "meaning_tamil": "நல்லொழுக்கம், நல்வழி",
        "meaning_english": "Virtue, righteousness",
    },
    {
        "word": "இன்பம்",
        "normalized_word": "இன்பம்",
        "transliteration": "Inbam",
        "part_of_speech": "Noun",
        "meaning_tamil": "மகிழ்ச்சி, சுகம்",
        "meaning_english": "Happiness, pleasure",
    },
    {
        "word": "துன்பம்",
        "normalized_word": "துன்பம்",
        "transliteration": "Thunbam",
        "part_of_speech": "Noun",
        "meaning_tamil": "துயரம், வருத்தம்",
        "meaning_english": "Sorrow, suffering",
    },
    {
        "word": "வீரம்",
        "normalized_word": "வீரம்",
        "transliteration": "Veeram",
        "part_of_speech": "Noun",
        "meaning_tamil": "துணிவு, தைரியம்",
        "meaning_english": "Courage, bravery",
    },
]


# ============================================================
# RELATION DATA
# ============================================================

relations_data = [
    ("அன்பு", "பாசம்", "synonym"),
    ("அன்பு", "நேசம்", "synonym"),
    ("பாசம்", "அன்பு", "synonym"),
    ("நேசம்", "அன்பு", "synonym"),

    ("அன்பு", "வெறுப்பு", "antonym"),
    ("வெறுப்பு", "அன்பு", "antonym"),

    ("அன்பு", "நட்பு", "related"),
    ("நட்பு", "அன்பு", "related"),
]


# ============================================================
# LITERARY WORK DATA
# ============================================================

literary_data = [
    {
        "title": "திருக்குறள்",
        "author": "திருவள்ளுவர்",
        "period": "சங்கம் மருவிய காலம்",
        "genre": "Ethics",
        "chapter": "அன்புடைமை",
        "passage": "அன்பு மனித வாழ்க்கையின் அடிப்படை பண்பாகக் கருதப்படுகிறது.",
        "word": "அன்பு"
    },
    {
        "title": "தமிழ் இலக்கிய எடுத்துக்காட்டு",
        "author": "Demo Literary Corpus",
        "period": "Classical Tamil",
        "genre": "Literature",
        "chapter": "அன்பு",
        "passage": "அன்பு, நட்பு, அறம் ஆகியவை மனித உறவுகளின் முக்கிய கூறுகளாகும்.",
        "word": "அன்பு"
    }
]


# ============================================================
# DATABASE
# ============================================================

db = SessionLocal()

try:

    # ========================================================
    # ADD WORDS
    # ========================================================

    print("\nAdding words...\n")

    for item in words_data:

        existing_word = (
            db.query(Word)
            .filter(Word.word == item["word"])
            .first()
        )

        if existing_word:
            print(f"Word already exists: {item['word']}")
            continue

        word = Word(
            word=item["word"],
            normalized_word=item["normalized_word"],
            transliteration=item["transliteration"],
            part_of_speech=item["part_of_speech"],
            source="Demo Dataset"
        )

        db.add(word)
        db.flush()

        meaning = Meaning(
            word_id=word.id,
            meaning_tamil=item["meaning_tamil"],
            meaning_english=item["meaning_english"],
            source="Demo Dataset"
        )

        db.add(meaning)

        print(f"Added word: {item['word']}")

    db.commit()


    # ========================================================
    # ADD RELATIONS
    # ========================================================

    print("\nAdding relationships...\n")

    for source_word, target_word, relation_type in relations_data:

        source = (
            db.query(Word)
            .filter(Word.word == source_word)
            .first()
        )

        target = (
            db.query(Word)
            .filter(Word.word == target_word)
            .first()
        )

        if not source or not target:
            continue

        existing_relation = (
            db.query(Relation)
            .filter(
                Relation.word_id == source.id,
                Relation.related_word_id == target.id,
                Relation.relation_type == relation_type
            )
            .first()
        )

        if existing_relation:
            print(
                f"Relation already exists: "
                f"{source_word} → {relation_type} → {target_word}"
            )
            continue

        relation = Relation(
            word_id=source.id,
            related_word_id=target.id,
            relation_type=relation_type,
            confidence=1.0,
            source="Demo Dataset"
        )

        db.add(relation)

        print(
            f"Added relation: "
            f"{source_word} → {relation_type} → {target_word}"
        )

    db.commit()


    # ========================================================
    # ADD LITERATURE
    # ========================================================

    print("\nAdding literary data...\n")

    for item in literary_data:

        word = (
            db.query(Word)
            .filter(Word.word == item["word"])
            .first()
        )

        if not word:
            print(f"Word not found: {item['word']}")
            continue

        # Check whether this literary work already exists
        work = (
            db.query(LiteraryWork)
            .filter(
                LiteraryWork.title == item["title"],
                LiteraryWork.author == item["author"]
            )
            .first()
        )

        if not work:

            work = LiteraryWork(
                title=item["title"],
                author=item["author"],
                period=item["period"],
                genre=item["genre"],
                source="Demo Literary Dataset"
            )

            db.add(work)
            db.flush()

        # Create passage
        passage = LiteraryPassage(
            work_id=work.id,
            chapter=item["chapter"],
            passage=item["passage"]
        )

        db.add(passage)
        db.flush()

        # Create occurrence
        occurrence = WordOccurrence(
            word_id=word.id,
            passage_id=passage.id
        )

        db.add(occurrence)

        print(
            f"Added literary passage: "
            f"{item['title']}"
        )

    db.commit()

    print("\n========================================")
    print("All demo data added successfully!")
    print("========================================\n")


except Exception as e:

    db.rollback()

    print("\nERROR:")
    print(e)


finally:

    db.close()