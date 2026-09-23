from literary_search import TamilLiterarySearch


CSV_PATH = "data/processed/literary_passages.csv"


search_engine = TamilLiterarySearch(
    CSV_PATH
)


queries = [
    "அன்பு",
    "கல்வி",
    "அறம்"
]


for query in queries:

    print("\n" + "=" * 60)

    print("SEARCH:", query)

    print("=" * 60)

    results = search_engine.search(
        query,
        top_k=3
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {i}")

        print("Score:", result["score"])

        print("Work:", result["work"])

        print("Author:", result["author"])

        print("Period:", result["period"])

        print("Theme:", result["theme"])

        print("Text:", result["text"])

        print("Source:", result["source"])