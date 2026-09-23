import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


MODEL_NAME = "Tamil-ai/tamil-embed-base"


class TamilLiterarySearch:

    def __init__(self, csv_path):

        print("Loading literary dataset...")

        self.data = pd.read_csv(csv_path)

        self.data["text"] = self.data["text"].fillna("")

        print(
            f"Loaded {len(self.data)} literary passages."
        )

        print("Loading Tamil embedding model...")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Model loaded successfully.")

        # The model is trained for retrieval.
        # "passage:" helps identify database text.
        passages = [
            "passage: " + text
            for text in self.data["text"]
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

        print("Building FAISS index...")

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.index.add(embeddings)

        print("Literary search engine ready!")


    def search(self, query, top_k=5):

        query_text = "query: " + query

        query_embedding = self.model.encode(
            [query_text],
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

        for score, index in zip(
            scores[0],
            indexes[0]
        ):

            if index == -1:
                continue

            row = self.data.iloc[index]

            results.append({
                "text": row["text"],
                "work": row["work"],
                "author": row["author"],
                "period": row["period"],
                "theme": row["theme"],
                "source": row["source"],
                "score": round(
                    float(score),
                    4
                )
            })

        return results