import unicodedata


def normalize_tamil(text: str) -> str:
    """
    Normalize Tamil text using Unicode NFC normalization.

    This helps ensure that visually identical Tamil words
    are stored and searched consistently.
    """

    if not text:
        return ""

    # Remove leading/trailing whitespace
    text = text.strip()

    # Normalize Unicode representation
    text = unicodedata.normalize("NFC", text)

    # Convert multiple spaces into a single space
    text = " ".join(text.split())

    return text