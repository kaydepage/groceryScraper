import pandas as pd
from pathlib import Path

pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)

def load_all_products(path=""):
    dfs = []
    for csv in Path(path).glob("*products.csv"):
        df = pd.read_csv(csv)
        # df["supermarket"] = csv.stem  # e.g. "coles", "woolworths"
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def search_products(keyword, df):
    results = df[df["Name"].str.contains(keyword, case=False, na=False)]
    return results[["Name", "Price", "Price/KG", "URL"]].sort_values("Price")

# Load data once
all_products = load_all_products()

# Search example
results = search_products("red rock", all_products)
print(results)
