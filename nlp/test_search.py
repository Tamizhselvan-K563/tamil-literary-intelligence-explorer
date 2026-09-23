from semantic_search import TamilSemanticSearch


search_engine = TamilSemanticSearch(
    "data/processed/words.csv"
)


query = "இன்பம்"


results = search_engine.search(
    query,
    top_k=5
)


print("\nSearch:", query)
print("\nResults:")

for result in results:
    print(
        result["word"],
        "|",
        result["meaning_tamil"],
        "| Score:",
        result["score"]
    )