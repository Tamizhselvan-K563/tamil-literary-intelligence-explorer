import pandas as pd

words = pd.read_csv("data/processed/words.csv")

relations = pd.read_csv("data/processed/relations.csv")

print("Number of words:", len(words))
print("Number of relations:", len(relations))

print("\nWords:")
print(words[["word", "meaning_tamil"]])

print("\nRelations:")
print(relations)