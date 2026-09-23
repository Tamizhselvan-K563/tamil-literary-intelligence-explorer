from sentence_transformers import SentenceTransformer


MODEL_NAME = "Tamil-ai/tamil-embed-base"


def load_model():
    print("Loading Tamil embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded successfully.")
    return model


def create_embeddings(model, texts):
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings