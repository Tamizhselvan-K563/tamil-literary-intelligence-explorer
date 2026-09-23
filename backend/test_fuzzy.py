from utils.fuzzy import similarity_score


words = [
    "அன்பு",
    "பாசம்",
    "நேசம்",
    "நட்பு",
    "வெறுப்பு"
]


query = "அன்னுப்பு"


print("Query:", query)
print()
print("Similarity scores:")
print("-" * 40)


for word in words:

    score = similarity_score(
        query,
        word
    )

    print(f"{word} → {score:.2f}")