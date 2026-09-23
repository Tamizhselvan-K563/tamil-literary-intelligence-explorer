from embeddings import load_model, create_embeddings
from faiss_search import TamilFaissSearch


texts = [
    "அன்பு என்பது உயர்ந்த பண்பு.",
    "நேசம் மனிதர்களை இணைக்கிறது.",
    "வெறுப்பு ஒரு எதிர்மறையான உணர்வு.",
    "தமிழ் இலக்கியம் பல நூற்றாண்டுகளின் செல்வமாகும்.",
    "நட்பு வாழ்க்கையில் முக்கியமான உறவாகும்."
]


print("Loading model...")

model = load_model()


print("\nCreating embeddings...")

embeddings = create_embeddings(
    model,
    texts
)


print("\nBuilding FAISS index...")

search_engine = TamilFaissSearch(
    embeddings,
    texts
)


query = "மனிதர்களுக்கிடையிலான பாசம்"


print("\nSearching for:")
print(query)


query_embedding = create_embeddings(
    model,
    [query]
)[0]


results = search_engine.search(
    query_embedding,
    top_k=3
)


print("\nTop results:")

for result in results:

    print(
        f"{result['score']} -> "
        f"{result['text']}"
    )