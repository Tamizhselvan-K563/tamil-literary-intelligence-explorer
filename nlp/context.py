import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "Tamil-ai/tamil-embed-base"


class TamilContextAnalyzer:

    def __init__(self, words_path="data/processed/words.csv"):

        print("Loading Tamil context analyzer...")

        self.words = pd.read_csv(words_path)

        self.words["word"] = self.words["word"].fillna("")
        self.words["meaning_tamil"] = self.words["meaning_tamil"].fillna("")
        self.words["meaning_english"] = self.words["meaning_english"].fillna("")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Context analyzer ready.")

    def analyze(self, word, context):

        matches = self.words[
            self.words["word"] == word
        ]

        if matches.empty:
            return {
                "word": word,
                "context": context,
                "message": "Word not found in dictionary."
            }

        row = matches.iloc[0]

        tamil_meanings = str(
            row["meaning_tamil"]
        ).split(";")

        english_meanings = str(
            row["meaning_english"]
        ).split(";")

        meaning_texts = [
            f"{word}: {meaning}"
            for meaning in tamil_meanings
        ]

        context_embedding = self.model.encode(
            [f"query: {context}"],
            normalize_embeddings=True
        )

        meaning_embeddings = self.model.encode(
            [
                f"passage: {meaning}"
                for meaning in meaning_texts
            ],
            normalize_embeddings=True
        )

        scores = cosine_similarity(
            context_embedding,
            meaning_embeddings
        )[0]

        best_index = int(np.argmax(scores))

        best_tamil = tamil_meanings[best_index]

        best_english = ""

        if best_index < len(english_meanings):
            best_english = english_meanings[best_index]

        return {
            "word": word,
            "context": context,
            "meaning_tamil": best_tamil,
            "meaning_english": best_english,
            "confidence": round(
                float(scores[best_index]),
                4
            )
        }