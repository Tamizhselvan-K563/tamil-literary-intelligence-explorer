from embeddings import load_model, create_embeddings


texts = [
    "அன்பு என்பது உயர்ந்த பண்பு.",
    "நேசம் மனிதர்களை இணைக்கிறது.",
    "வெறுப்பு ஒரு எதிர்மறையான உணர்வு.",
    "தமிழ் இலக்கியம் பல நூற்றாண்டுகளின் செல்வமாகும்."
]


model = load_model()

embeddings = create_embeddings(model, texts)

print("\nEmbedding shape:")
print(embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0])