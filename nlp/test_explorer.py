from explorer_engine import TamilLiteraryExplorer


explorer = TamilLiteraryExplorer()


word = "அன்பு"


result = explorer.search(
    word,
    top_k=3
)


print("\n")
print("=" * 60)
print("TAMIL LITERARY INTELLIGENCE EXPLORER")
print("=" * 60)


print("\nWORD")
print(result["word"])


print("\nTAMIL MEANINGS")

for meaning in result["meanings_tamil"]:
    print("-", meaning)


print("\nENGLISH MEANINGS")

for meaning in result["meanings_english"]:
    print("-", meaning)


print("\nWORD RELATIONSHIPS")

for relation in result["relationships"]:

    print(
        f"- {relation['word']} "
        f"[{relation['relation']}] "
        f"(score: {relation['confidence']})"
    )


print("\nLITERARY RESULTS")


for i, literary in enumerate(
    result["literary_results"],
    start=1
):

    print("\n" + "-" * 60)

    print("Result:", i)

    print(
        "Text:",
        literary["literary_text"]
    )

    print(
        "Work:",
        literary["work"]
    )

    print(
        "Author:",
        literary["author"]
    )

    print(
        "Period:",
        literary["period"]
    )

    print(
        "Theme:",
        literary["theme"]
    )

    print(
        "Meaning:",
        literary["meaning_tamil"]
    )

    print(
        "English Meaning:",
        literary["meaning_english"]
    )

    print(
        "Literary Score:",
        literary["literary_score"]
    )

    print(
        "Meaning Score:",
        literary["meaning_score"]
    )