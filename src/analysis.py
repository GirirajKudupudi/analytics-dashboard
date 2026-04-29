import pandas as pd
import numpy as np
from scipy import stats

def run_statistical_analysis(df):
    """Perform statistical tests on the Zomato data."""
    results = {}

    # ---- 1. Does online ordering affect ratings? (t-test) ----
    print("=" * 50)
    print("TEST 1: Online Order vs Ratings (t-test)")
    print("=" * 50)
    online_ratings = df[df['online_order'] == True]['rating']
    no_online_ratings = df[df['online_order'] == False]['rating']
    t_stat, p_val = stats.ttest_ind(online_ratings, no_online_ratings)
    results['online_vs_rating'] = {
        'online_avg': round(online_ratings.mean(), 3),
        'no_online_avg': round(no_online_ratings.mean(), 3),
        't_statistic': round(t_stat, 4),
        'p_value': round(p_val, 6),
        'significant': p_val < 0.05
    }
    print(f"Online order avg rating: {results['online_vs_rating']['online_avg']}")
    print(f"No online avg rating: {results['online_vs_rating']['no_online_avg']}")
    print(f"t-statistic: {t_stat:.4f}, p-value: {p_val:.6f}")
    print(f"Significant difference: {'YES' if p_val < 0.05 else 'NO'}")

    # ---- 2. Does cost correlate with rating? (Pearson) ----
    print("\n" + "=" * 50)
    print("TEST 2: Cost vs Rating (Pearson Correlation)")
    print("=" * 50)
    corr, p_corr = stats.pearsonr(df['cost'].dropna(), df.loc[df['cost'].notna(), 'rating'])
    results['cost_vs_rating'] = {
        'correlation': round(corr, 4),
        'p_value': round(p_corr, 6),
        'strength': 'Strong' if abs(corr) > 0.5 else 'Moderate' if abs(corr) > 0.3 else 'Weak'
    }
    print(f"Correlation: {corr:.4f}")
    print(f"p-value: {p_corr:.6f}")
    print(f"Strength: {results['cost_vs_rating']['strength']}")

    # ---- 3. Does book_table affect ratings? (t-test) ----
    print("\n" + "=" * 50)
    print("TEST 3: Book Table vs Ratings (t-test)")
    print("=" * 50)
    book_ratings = df[df['book_table'] == True]['rating']
    no_book_ratings = df[df['book_table'] == False]['rating']
    t_stat2, p_val2 = stats.ttest_ind(book_ratings, no_book_ratings)
    results['book_table_vs_rating'] = {
        'book_avg': round(book_ratings.mean(), 3),
        'no_book_avg': round(no_book_ratings.mean(), 3),
        't_statistic': round(t_stat2, 4),
        'p_value': round(p_val2, 6),
        'significant': p_val2 < 0.05
    }
    print(f"Book table avg rating: {results['book_table_vs_rating']['book_avg']}")
    print(f"No book table avg rating: {results['book_table_vs_rating']['no_book_avg']}")
    print(f"Significant difference: {'YES' if p_val2 < 0.05 else 'NO'}")

    # ---- 4. Restaurant type vs rating (ANOVA - multiple groups) ----
    print("\n" + "=" * 50)
    print("TEST 4: Restaurant Type vs Rating (ANOVA)")
    print("=" * 50)
    top_types = df['restaurant_type'].value_counts().head(5).index
    groups = [df[df['restaurant_type'] == t]['rating'] for t in top_types]
    f_stat, p_anova = stats.f_oneway(*groups)
    results['type_vs_rating'] = {
        'f_statistic': round(f_stat, 4),
        'p_value': round(p_anova, 6),
        'significant': p_anova < 0.05
    }
    print(f"F-statistic: {f_stat:.4f}")
    print(f"p-value: {p_anova:.6f}")
    print(f"Groups tested: {list(top_types)}")
    print(f"Significant difference between types: {'YES' if p_anova < 0.05 else 'NO'}")

    # ---- 5. Does more cuisines = better rating? (Pearson) ----
    print("\n" + "=" * 50)
    print("TEST 5: Number of Cuisines vs Rating")
    print("=" * 50)
    corr2, p_corr2 = stats.pearsonr(df['cuisine_count'], df['rating'])
    results['cuisines_vs_rating'] = {
        'correlation': round(corr2, 4),
        'p_value': round(p_corr2, 6)
    }
    print(f"Correlation: {corr2:.4f}")
    print(f"p-value: {p_corr2:.6f}")
    print(f"More cuisines = {'higher' if corr2 > 0 else 'lower'} ratings")

    return results


if __name__ == "__main__":
    df = pd.read_csv('data/processed/zomato_cleaned.csv')
    print(f"Loaded {len(df)} rows\n")
    results = run_statistical_analysis(df)
    print("\n\nAll statistical tests completed!")