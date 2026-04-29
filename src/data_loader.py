import pandas as pd

def load_data(filepath='data/raw/zomato.csv'):
    """Load the Zomato dataset."""
    df = pd.read_csv(filepath, encoding='latin-1')
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    df = load_data()
    print(df.head())