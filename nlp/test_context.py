from context import TamilContextAnalyzer


analyzer = TamilContextAnalyzer()


word = "அகம்"

context = (
    "அவன் தனது அகத்தை ஆராய்ந்து "
    "தன் எண்ணங்களைப் புரிந்துகொண்டான்."
)


result = analyzer.analyze(
    word,
    context
)


print("\nContextual Meaning Result")
print("-------------------------")

print("Word:", result["word"])

print("Context:", result["context"])

print(
    "Tamil Meaning:",
    result.get("meaning_tamil")
)

print(
    "English Meaning:",
    result.get("meaning_english")
)

print(
    "Confidence:",
    result.get("confidence")
)