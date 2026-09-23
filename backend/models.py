from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True, nullable=False, index=True)
    normalized_word = Column(String, nullable=False, index=True)
    transliteration = Column(String, nullable=True)
    part_of_speech = Column(String, nullable=True)
    source = Column(String, nullable=True)

    meanings = relationship(
        "Meaning",
        back_populates="word"
    )


class Meaning(Base):
    __tablename__ = "meanings"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    meaning_tamil = Column(Text, nullable=False)
    meaning_english = Column(Text, nullable=True)
    source = Column(String, nullable=True)

    word = relationship(
        "Word",
        back_populates="meanings"
    )


class Relation(Base):
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    related_word_id = Column(Integer, ForeignKey("words.id"))
    relation_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    source = Column(String, nullable=True)


class LiteraryWork(Base):
    __tablename__ = "literary_works"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    period = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    source = Column(String, nullable=True)


class LiteraryPassage(Base):
    __tablename__ = "literary_passages"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(Integer, ForeignKey("literary_works.id"))
    chapter = Column(String, nullable=True)
    passage = Column(Text, nullable=False)


class WordOccurrence(Base):
    __tablename__ = "word_occurrences"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    passage_id = Column(Integer, ForeignKey("literary_passages.id"))
    start_position = Column(Integer, nullable=True)
    end_position = Column(Integer, nullable=True)