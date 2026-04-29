import pandas as pd
import numpy as np

def clean_data(df):
    """Clean the Zomato dataset and create useful features."""
    df = df.copy()
    print(f"Starting shape: {df.shape}")

    # ---- 1. Clean the rate column ----
    # Remove "/5", strip spaces, handle "NEW" and "-"
    df['rate'] = df['rate'].str.replace('/5', '', regex=False)
    df['rate'] = df['rate'].str.strip()
    df['rate'] = df['rate'].replace(['NEW', '-', ''], np.nan)
    df['rate'] = df['rate'].astype(float)
    print(f"Ratings cleaned: {df['rate'].notna().sum()} valid ratings")

    # ---- 2. Clean the cost column ----
    # Remove commas and convert to number
    df['cost'] = df['approx_cost(for two people)'].str.replace(',', '', regex=False)
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
    print(f"Cost cleaned: {df['cost'].notna().sum()} valid costs")

    # ---- 3. Clean online_order and book_table to boolean ----
    df['online_order'] = df['online_order'].map({'Yes': True, 'No': False})
    df['book_table'] = df['book_table'].map({'Yes': True, 'No': False})

    # ---- 4. Handle missing values ----
    df['dish_liked'] = df['dish_liked'].fillna('Not Available')
    df['cuisines'] = df['cuisines'].fillna('Unknown')
    df['rest_type'] = df['rest_type'].fillna('Unknown')
    df['location'] = df['location'].fillna('Unknown')

    # Drop rows with no rating AND no cost (not useful)
    before = len(df)
    df = df.dropna(subset=['rate', 'cost'], how='all')
    print(f"Dropped {before - len(df)} rows with no rating AND no cost")

    # Fill remaining missing ratings with median
    df['rate'] = df['rate'].fillna(df['rate'].median())
    df['cost'] = df['cost'].fillna(df['cost'].median())

    # ---- 5. Create new features ----
    # Price category
    df['price_category'] = pd.cut(
        df['cost'],
        bins=[0, 200, 500, 1000, 5000],
        labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
    )

    # Number of cuisines offered
    df['cuisine_count'] = df['cuisines'].str.split(',').str.len()

    # Primary cuisine (first one listed)
    df['primary_cuisine'] = df['cuisines'].str.split(',').str[0].str.strip()

    # Rating category
    df['rating_category'] = pd.cut(
        df['rate'],
        bins=[0, 2.5, 3.5, 4.0, 5.0],
        labels=['Poor', 'Average', 'Good', 'Excellent']
    )

    # ---- 6. Drop unnecessary columns ----
    df = df.drop(columns=['url', 'phone', 'menu_item', 'reviews_list',
                           'approx_cost(for two people)'])

    # ---- 7. Rename columns for clarity ----
    df = df.rename(columns={
        'name': 'restaurant_name',
        'rate': 'rating',
        'listed_in(type)': 'listing_type',
        'listed_in(city)': 'city_area',
        'rest_type': 'restaurant_type'
    })

    print(f"\nFinal shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # ---- 8. Save cleaned data ----
    df.to_csv('data/processed/zomato_cleaned.csv', index=False)
    print(f"\nCleaned data saved to data/processed/zomato_cleaned.csv")

    return df


if __name__ == "__main__":
    from src.data_loader import load_data
    df = load_data()
    df_clean = clean_data(df)
    print(f"\nSample of cleaned data:")
    print(df_clean.head())