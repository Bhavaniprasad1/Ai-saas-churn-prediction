import pandas as pd

df = pd.read_csv("data/churn_data.csv")
df.columns = df.columns.str.replace(" ", "_")
df.columns = df.columns.str.replace("-", "_")
df.columns = df.columns.str.strip()

print(df.columns.tolist())
