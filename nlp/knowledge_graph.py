import pandas as pd
import networkx as nx


class TamilKnowledgeGraph:

    def __init__(
        self,
        relations_path="data/processed/relations.csv"
    ):

        print("Loading Tamil relationship data...")

        # Load relationship data
        self.data = pd.read_csv(
            relations_path
        )

        # Create graph
        self.graph = nx.Graph()

        # Build graph
        self._build_graph()

        print(
            f"Knowledge graph ready: "
            f"{self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges."
        )

    # =====================================================
    # BUILD KNOWLEDGE GRAPH
    # =====================================================

    def _build_graph(self):

        for _, row in self.data.iterrows():

            word = str(
                row["word"]
            )

            related_word = str(
                row["related_word"]
            )

            relation = str(
                row["relation"]
            )

            confidence = float(
                row["confidence"]
            )

            # Add words as nodes
            self.graph.add_node(
                word
            )

            self.graph.add_node(
                related_word
            )

            # Connect words
            self.graph.add_edge(
                word,
                related_word,
                relation=relation,
                confidence=confidence
            )

    # =====================================================
    # GET RELATED WORDS
    # =====================================================

    def get_related_words(
        self,
        word
    ):

        # Word doesn't exist
        if word not in self.graph:

            return []

        results = []

        # Find connected words
        for related_word in (
            self.graph.neighbors(word)
        ):

            edge = self.graph[
                word
            ][related_word]

            results.append({

                "word": related_word,

                "relation": edge[
                    "relation"
                ],

                "confidence": edge[
                    "confidence"
                ]
            })

        return results