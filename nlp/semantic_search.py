import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TamilSemanticSearch:

    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)

        # Combine Tamil word and Tamil meaning
        self.data["search_text"] = (
            self.data["word"].fillna("")
            + " "
            + self.data["meaning_tamil"].fillna("")
        )

        # Character-based TF-IDF works reasonably well
        # for Tamil text without requiring tokenization.
        self.vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(2, 5)
        )

        self.matrix = self.vectorizer.fit_transform(
            self.data["search_text"]
        )

    def search(self, query, top_k=5):

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix
        ).flatten()

        indexes = scores.argsort()[-top_k:][::-1]

        results = []

        for index in indexes:

            results.append({
                "word": self.data.iloc[index]["word"],
                "meaning_tamil": self.data.iloc[index]["meaning_tamil"],
                "meaning_english": self.data.iloc[index]["meaning_english"],
                "score": round(float(scores[index]), 4)
            })

        return results