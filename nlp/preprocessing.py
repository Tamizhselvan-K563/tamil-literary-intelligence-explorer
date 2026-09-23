import unicodedata
import re


def normalize_tamil(text):
    """
    Normalize Tamil Unicode text and remove
    unnecessary spaces.
    """

    if not text:
        return ""

    # Normalize Unicode
    text = unicodedata.normalize("NFC", text)

    # Remove leading/trailing spaces
    text = text.strip()

    # Replace multiple spaces with one
    text = re.sub(r"\s+", " ", text)

    return text