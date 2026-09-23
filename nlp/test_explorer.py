from explorer_engine import TamilLiteraryExplorer


explorer = TamilLiteraryExplorer()


word = "அன்பு"


print("\n")
print("=" * 60)
print("TAMIL LITERARY EXPLORER")
print("=" * 60)

print("\nSearch word:", word)


results = explorer.search(
    word,
    top_k=3
)


for i, result in enumerate(
    results,
    start=1
):

    print("\n" + "-" * 60)

    print("RESULT", i)

    print("Word:", result["word"])

    print(
        "Tamil Meaning:",
        result["meaning_tamil"]
    )

    print(
        "English Meaning:",
        result["meaning_english"]
    )

    print(
        "Literary Text:",
        result["literary_text"]
    )

    print(
        "Work:",
        result["work"]
    )

    print(
        "Author:",
        result["author"]
    )

    print(
        "Period:",
        result["period"]
    )

    print(
        "Theme:",
        result["theme"]
    )

    print(
        "Literary Similarity:",
        result["literary_score"]
    )

    print(
        "Meaning Similarity:",
        result["meaning_score"]
    )