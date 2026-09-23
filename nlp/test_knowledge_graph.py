from knowledge_graph import TamilKnowledgeGraph


graph = TamilKnowledgeGraph()


word = "அன்பு"


print("\n")
print("=" * 60)
print("TAMIL KNOWLEDGE GRAPH")
print("=" * 60)

print("\nSearch word:", word)

results = graph.get_related_words(
    word
)


print("\nRelated words:")

for result in results:

    print(
        f"{result['word']} "
        f"-> {result['relation']} "
        f"(confidence: "
        f"{result['confidence']})"
    )