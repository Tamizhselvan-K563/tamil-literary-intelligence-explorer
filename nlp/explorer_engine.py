import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "Tamil-ai/tamil-embed-base"


class TamilLiteraryExplorer:

    def __init__(
        self,
        words_path="data/processed/words.csv",
        literary_path="data/processed/literary_passages.csv"
    ):

        print("Loading Tamil Literary Explorer...")

        # Load word data
        self.words = pd.read_csv(words_path)

        self.words["word"] = self.words["word"].fillna("")
        self.words["meaning_tamil"] = (
            self.words["meaning_tamil"].fillna("")
        )
        self.words["meaning_english"] = (
            self.words["meaning_english"].fillna("")
        )

        # Load literary data
        self.literature = pd.read_csv(
            literary_path
        )

        self.literature["text"] = (
            self.literature["text"].fillna("")
        )

        print(
            f"Loaded {len(self.literature)} literary passages."
        )

        # Load model only once
        print("Loading Tamil embedding model...")

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        print("Model loaded successfully.")

        # Create passage embeddings
        passages = [
            "passage: " + text
            for text in self.literature["text"]
        ]

        print("Creating literary embeddings...")

        embeddings = self.model.encode(
            passages,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.dimension = embeddings.shape[1]

        # Create FAISS index
        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.index.add(embeddings)

        print("Tamil Literary Explorer ready!")

    def search(self, word, top_k=3):

        # Search literature
        query_embedding = self.model.encode(
            ["query: " + word],
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        scores, indexes = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        # Find word meanings
        matches = self.words[
            self.words["word"] == word
        ]

        if matches.empty:

            meanings_tamil = []
            meanings_english = []

        else:

            row = matches.iloc[0]

            meanings_tamil = str(
                row["meaning_tamil"]
            ).split(";")

            meanings_english = str(
                row["meaning_english"]
            ).split(";")

        # Analyze each literary result
        for score, index in zip(
            scores[0],
            indexes[0]
        ):

            if index == -1:
                continue

            row = self.literature.iloc[index]

            context = row["text"]

            selected_tamil = ""
            selected_english = ""
            meaning_score = None

            if meanings_tamil:

                meaning_texts = [
                    f"{word}: {meaning}"
                    for meaning in meanings_tamil
                ]

                context_embedding = self.model.encode(
                    ["query: " + context],
                    normalize_embeddings=True
                )

                meaning_embeddings = self.model.encode(
                    [
                        "passage: " + meaning
                        for meaning in meaning_texts
                    ],
                    normalize_embeddings=True
                )

                meaning_scores = cosine_similarity(
                    context_embedding,
                    meaning_embeddings
                )[0]

                best_index = int(
                    np.argmax(meaning_scores)
                )

                selected_tamil = (
                    meanings_tamil[best_index]
                )

                if best_index < len(
                    meanings_english
                ):
                    selected_english = (
                        meanings_english[best_index]
                    )

                meaning_score = round(
                    float(meaning_scores[best_index]),
                    4
                )

            results.append({

                "word": word,

                "meaning_tamil": selected_tamil,

                "meaning_english": selected_english,

                "literary_text": context,

                "work": row["work"],

                "author": row["author"],

                "period": row["period"],

                "theme": row["theme"],

                "source": row["source"],

                "literary_score": round(
                    float(score),
                    4
                ),

                "meaning_score": meaning_score
            })

        return results