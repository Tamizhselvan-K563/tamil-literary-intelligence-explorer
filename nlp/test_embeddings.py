from embeddings import load_model, create_embeddings


model = load_model()


texts = [
    "அன்பு என்பது ஒரு நல்ல உணர்வு.",
    "பாசம் மனிதர்களை இணைக்கிறது.",
    "வெறுப்பு ஒரு எதிர்மறையான உணர்வு.",
    "தமிழ் இலக்கியம் மிகவும் பழமையானது."
]


embeddings = create_embeddings(model, texts)


print("\nEmbedding shape:")
print(embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0][:10])