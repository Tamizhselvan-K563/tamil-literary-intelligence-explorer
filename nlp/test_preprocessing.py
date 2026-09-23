from preprocessing import normalize_tamil


text = "  அன்பு    என்பது    மிகவும்    முக்கியமானது  "

result = normalize_tamil(text)

print("Original:")
print(text)

print("\nNormalized:")
print(result)