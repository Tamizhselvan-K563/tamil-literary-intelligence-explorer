import pandas as pd


path = "data/processed/literary_passages.csv"

data = pd.read_csv(path)

print("Number of passages:", len(data))

print("\nColumns:")
print(data.columns.tolist())

print("\nFirst passage:")
print(data.iloc[0]["text"])

print("\nWorks:")
print(data["work"].unique())