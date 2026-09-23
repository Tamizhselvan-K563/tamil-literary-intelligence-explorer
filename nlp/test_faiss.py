from embeddings import load_model
from faiss_search import TamilFaissSearch


texts = [
    "அன்பு என்பது ஒரு நல்ல உணர்வு.",
    "பாசம் மனிதர்களை இணைக்கிறது.",
    "காதல் மனிதர்களின் வாழ்க்கையில் முக்கியமான உணர்வு.",
    "வெறுப்பு ஒரு எதிர்மறையான உணர்வு.",
    "தமிழ் இலக்கியம் மிகவும் பழமையானது."
]


print("Loading model...")

model = load_model()


print("Creating embeddings...")

embeddings = model.encode(
    texts,
    normalize_embeddings=True
)


search_engine = TamilFaissSearch(
    embeddings,
    texts
)


query = "அன்பும் காதலும்"


query_embedding = model.encode(
    [query],
    normalize_embeddings=True
)[0]


results = search_engine.search(
    query_embedding,
    top_k=3
)


print("\nQuery:")
print(query)

print("\nSemantic results:")

for result in results:

    print(
        result["score"],
        "|",
        result["text"]
    )