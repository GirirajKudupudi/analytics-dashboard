import pandas as pd
import sqlite3

def setup_database(df, db_path='data/processed/zomato.db'):
    """Load cleaned data into SQLite for SQL practice."""
    conn = sqlite3.connect(db_path)
    df.to_sql('restaurants', conn, if_exists='replace', index=False)
    print(f"Database created with {len(df)} rows")
    return conn


def run_queries(conn):
    """Run analysis queries and return results."""
    results = {}

    # ---- Query 1: Top 10 areas by number of restaurants ----
    print("\n" + "=" * 50)
    print("QUERY 1: Top 10 Areas by Restaurant Count")
    print("=" * 50)
    results['top_areas'] = pd.read_sql("""
        SELECT 
            city_area,
            COUNT(*) AS total_restaurants,
            ROUND(AVG(rating), 2) AS avg_rating,
            ROUND(AVG(cost), 0) AS avg_cost
        FROM restaurants
        GROUP BY city_area
        ORDER BY total_restaurants DESC
        LIMIT 10
    """, conn)
    print(results['top_areas'])

    # ---- Query 2: Best rated cuisines (with enough data) ----
    print("\n" + "=" * 50)
    print("QUERY 2: Top 10 Cuisines by Rating")
    print("=" * 50)
    results['top_cuisines'] = pd.read_sql("""
        SELECT 
            primary_cuisine,
            COUNT(*) AS restaurant_count,
            ROUND(AVG(rating), 2) AS avg_rating,
            ROUND(AVG(cost), 0) AS avg_cost
        FROM restaurants
        WHERE primary_cuisine != 'Unknown'
        GROUP BY primary_cuisine
        HAVING restaurant_count >= 50
        ORDER BY avg_rating DESC
        LIMIT 10
    """, conn)
    print(results['top_cuisines'])

    # ---- Query 3: Online order impact on ratings (CASE WHEN) ----
    print("\n" + "=" * 50)
    print("QUERY 3: Online Order vs No Online Order")
    print("=" * 50)
    results['online_impact'] = pd.read_sql("""
        SELECT 
            CASE 
                WHEN online_order = 1 THEN 'Online Order Available'
                ELSE 'No Online Order'
            END AS order_type,
            COUNT(*) AS total,
            ROUND(AVG(rating), 2) AS avg_rating,
            ROUND(AVG(cost), 0) AS avg_cost,
            ROUND(AVG(votes), 0) AS avg_votes
        FROM restaurants
        GROUP BY online_order
    """, conn)
    print(results['online_impact'])

    # ---- Query 4: Price category analysis with WINDOW FUNCTIONS ----
    print("\n" + "=" * 50)
    print("QUERY 4: Price Category Analysis (Window Functions)")
    print("=" * 50)
    results['price_analysis'] = pd.read_sql("""
        SELECT 
            price_category,
            restaurant_count,
            avg_rating,
            avg_votes,
            ROUND(restaurant_count * 100.0 / SUM(restaurant_count) OVER(), 2) 
                AS pct_of_total,
            RANK() OVER(ORDER BY avg_rating DESC) AS rating_rank
        FROM (
            SELECT 
                price_category,
                COUNT(*) AS restaurant_count,
                ROUND(AVG(rating), 2) AS avg_rating,
                ROUND(AVG(votes), 0) AS avg_votes
            FROM restaurants
            WHERE price_category IS NOT NULL
            GROUP BY price_category
        )
        ORDER BY rating_rank
    """, conn)
    print(results['price_analysis'])

    # ---- Query 5: Top restaurants per area using CTE + RANK ----
    print("\n" + "=" * 50)
    print("QUERY 5: Top Rated Restaurant in Each Area (CTE + RANK)")
    print("=" * 50)
    results['top_per_area'] = pd.read_sql("""
        WITH ranked_restaurants AS (
            SELECT 
                restaurant_name,
                city_area,
                rating,
                votes,
                cost,
                primary_cuisine,
                RANK() OVER(
                    PARTITION BY city_area 
                    ORDER BY rating DESC, votes DESC
                ) AS area_rank
            FROM restaurants
            WHERE votes >= 100
        )
        SELECT 
            restaurant_name,
            city_area,
            rating,
            votes,
            cost,
            primary_cuisine
        FROM ranked_restaurants
        WHERE area_rank = 1
        ORDER BY rating DESC
        LIMIT 15
    """, conn)
    print(results['top_per_area'])

    return results


if __name__ == "__main__":
    # Load cleaned data
    df = pd.read_csv('data/processed/zomato_cleaned.csv')
    conn = setup_database(df)
    results = run_queries(conn)
    conn.close()
    print("\n\nAll queries completed successfully!")