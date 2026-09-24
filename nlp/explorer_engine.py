import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.knowledge_graph import TamilKnowledgeGraph


MODEL_NAME = "Tamil-ai/tamil-embed-base"


class TamilLiteraryExplorer:

    def __init__(
        self,
        words_path="data/processed/words.csv",
        literary_path="data/processed/literary_passages.csv",
        relations_path="data/processed/relations.csv"
    ):

        print("Loading Tamil Literary Explorer...")

        # -----------------------------------
        # LOAD WORD DATA
        # -----------------------------------

        self.words = pd.read_csv(words_path)

        self.words["word"] = (
            self.words["word"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        self.words["meaning_tamil"] = (
            self.words["meaning_tamil"]
            .fillna("")
            .astype(str)
        )

        self.words["meaning_english"] = (
            self.words["meaning_english"]
            .fillna("")
            .astype(str)
        )

        print(
            f"Loaded {len(self.words)} words."
        )

        # -----------------------------------
        # LOAD LITERARY DATA
        # -----------------------------------

        self.literature = pd.read_csv(
            literary_path
        )

        self.literature["text"] = (
            self.literature["text"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        self.literature["theme"] = (
            self.literature["theme"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        self.literature["work"] = (
            self.literature["work"]
            .fillna("")
            .astype(str)
        )

        self.literature["author"] = (
            self.literature["author"]
            .fillna("")
            .astype(str)
        )

        self.literature["period"] = (
            self.literature["period"]
            .fillna("")
            .astype(str)
        )

        self.literature["source"] = (
            self.literature["source"]
            .fillna("")
            .astype(str)
        )

        print(
            f"Loaded {len(self.literature)} literary passages."
        )

        # -----------------------------------
        # LOAD KNOWLEDGE GRAPH
        # -----------------------------------

        self.knowledge_graph = (
            TamilKnowledgeGraph(
                relations_path
            )
        )

        # -----------------------------------
        # LOAD TAMIL EMBEDDING MODEL
        # -----------------------------------

        print("Loading Tamil embedding model...")

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        print("Model loaded successfully.")

        # -----------------------------------
        # CREATE LITERARY EMBEDDINGS
        # -----------------------------------

        print("Creating literary embeddings...")

        passages = [
            "passage: " + text
            for text in self.literature["text"]
        ]

        embeddings = self.model.encode(
            passages,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        # -----------------------------------
        # CREATE FAISS INDEX
        # -----------------------------------

        self.dimension = embeddings.shape[1]

        print("Building FAISS index...")

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.index.add(
            embeddings
        )

        print(
            "Tamil Literary Explorer ready!"
        )

    # =====================================================
    # MAIN SEARCH FUNCTION
    # =====================================================

    def search(
        self,
        word,
        top_k=3
    ):

        # -----------------------------------
        # CLEAN SEARCH WORD
        # -----------------------------------

        word = str(word).strip()

        # -----------------------------------
        # SEARCH QUERY EMBEDDING
        # -----------------------------------

        query_embedding = self.model.encode(
            ["query: " + word],
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        # -----------------------------------
        # SEARCH LITERATURE USING FAISS
        # -----------------------------------

        scores, indexes = self.index.search(
            query_embedding,
            top_k
        )

        # -----------------------------------
        # FIND WORD MEANINGS
        # -----------------------------------

        matches = self.words[
            self.words["word"] == word
        ]

        meanings_tamil = []
        meanings_english = []

        if not matches.empty:

            row = matches.iloc[0]

            meanings_tamil = [
                meaning.strip()
                for meaning in str(
                    row["meaning_tamil"]
                ).split(";")
                if meaning.strip()
            ]

            meanings_english = [
                meaning.strip()
                for meaning in str(
                    row["meaning_english"]
                ).split(";")
                if meaning.strip()
            ]

        # -----------------------------------
        # FIND WORD RELATIONSHIPS
        # -----------------------------------

        relationships = (
            self.knowledge_graph
            .get_related_words(word)
        )

        # -----------------------------------
        # PROCESS LITERARY RESULTS
        # -----------------------------------

        literary_results = []

        # ===================================
        # 1. EXACT THEME MATCH
        # ===================================

        exact_matches = self.literature[
            self.literature["theme"] == word
        ].head(top_k)

        for _, row in exact_matches.iterrows():

            literary_results.append({

                "literary_text": row["text"],

                "work": row["work"],

                "author": row["author"],

                "period": row["period"],

                "theme": row["theme"],

                "source": row["source"],

                "literary_score": 1.0,

                "meaning_tamil": (
                    meanings_tamil[0]
                    if meanings_tamil
                    else ""
                ),

                "meaning_english": (
                    meanings_english[0]
                    if meanings_english
                    else ""
                ),

                "meaning_score": None

            })

        # Store already-added passages
        existing_texts = {
            item["literary_text"]
            for item in literary_results
        }

        # ===================================
        # 2. SEMANTIC MATCH
        # ===================================

        for score, index in zip(
            scores[0],
            indexes[0]
        ):

            # Ignore invalid FAISS indexes
            if index == -1:
                continue

            # Ignore weak semantic matches
            if float(score) < 0.40:
                continue

            row = self.literature.iloc[index]

            context = row["text"]

            # Avoid duplicate passages
            if context in existing_texts:
                continue

            selected_tamil = ""
            selected_english = ""
            meaning_score = None

            # -----------------------------------
            # CONTEXTUAL MEANING
            # -----------------------------------

            if meanings_tamil:

                meaning_texts = [
                    f"{word}: {meaning}"
                    for meaning in meanings_tamil
                ]

                # Encode literary context
                context_embedding = (
                    self.model.encode(
                        ["query: " + context],
                        normalize_embeddings=True
                    )
                )

                # Encode possible meanings
                meaning_embeddings = (
                    self.model.encode(
                        [
                            "passage: " + meaning
                            for meaning in meaning_texts
                        ],
                        normalize_embeddings=True
                    )
                )

                # Compare context and meanings
                meaning_scores = (
                    cosine_similarity(
                        context_embedding,
                        meaning_embeddings
                    )[0]
                )

                # Select best meaning
                best_index = int(
                    np.argmax(
                        meaning_scores
                    )
                )

                selected_tamil = (
                    meanings_tamil[
                        best_index
                    ]
                )

                if best_index < len(
                    meanings_english
                ):
                    selected_english = (
                        meanings_english[
                            best_index
                        ]
                    )

                meaning_score = round(
                    float(
                        meaning_scores[
                            best_index
                        ]
                    ),
                    4
                )

            # -----------------------------------
            # ADD SEMANTIC RESULT
            # -----------------------------------

            literary_results.append({

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

                "meaning_tamil": selected_tamil,

                "meaning_english": selected_english,

                "meaning_score": meaning_score

            })

            existing_texts.add(context)

            # Keep result count controlled
            if len(literary_results) >= top_k:
                break

        # -----------------------------------
        # RETURN COMPLETE EXPLORER RESPONSE
        # -----------------------------------

        return {

            "word": word,

            "meanings_tamil": (
                meanings_tamil
            ),

            "meanings_english": (
                meanings_english
            ),

            "relationships": (
                relationships
            ),

            "literary_results": (
                literary_results
            )

        }