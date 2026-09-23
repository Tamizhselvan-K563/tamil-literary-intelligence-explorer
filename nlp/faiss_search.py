import faiss
import numpy as np


class TamilFaissSearch:

    def __init__(self, embeddings, texts):

        self.texts = texts

        # Convert embeddings to float32 for FAISS
        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.dimension = embeddings.shape[1]

        # Inner product works with normalized embeddings
        # as a cosine-similarity style search.
        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.index.add(embeddings)

    def search(self, query_embedding, top_k=3):

        query_embedding = np.asarray(
            [query_embedding],
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

            results.append({
                "text": self.texts[index],
                "score": round(float(score), 4)
            })

        return results