from difflib import SequenceMatcher

from utils.normalization import normalize_tamil


def similarity_score(text1: str, text2: str) -> float:
    """
    Calculate similarity between two Tamil strings.
    Returns a value between 0 and 1.
    """

    text1 = normalize_tamil(text1)
    text2 = normalize_tamil(text2)

    if not text1 or not text2:
        return 0.0

    return SequenceMatcher(
        None,
        text1,
        text2
    ).ratio()


def find_best_match(
    query: str,
    words: list,
    threshold: float = 0.65
):
    """
    Find the best matching word from a list of database words.

    A match is returned only when its similarity score
    reaches the threshold.
    """

    query = normalize_tamil(query)

    best_word = None
    best_score = 0.0

    for word in words:

        score = similarity_score(
            query,
            word.word
        )

        if score > best_score:
            best_score = score
            best_word = word

    if best_word and best_score >= threshold:
        return best_word, best_score

    return None, best_score