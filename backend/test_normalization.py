from utils.normalization import normalize_tamil


test_words = [
    "அன்பு",
    "  அன்பு  ",
    "நட்பு",
    "   அறம்   ",
]


for word in test_words:
    normalized = normalize_tamil(word)

    print("Original   :", repr(word))
    print("Normalized :", repr(normalized))
    print("-" * 40)