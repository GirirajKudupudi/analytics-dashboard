import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Page Config (MUST be first Streamlit command) ----
st.set_page_config(
    page_title='Zomato Bangalore Analytics',
    page_icon='🍽️',
    layout='wide'
)

# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/zomato_cleaned.csv')
    return df

df = load_data()

# ---- Sidebar Filters ----
st.sidebar.header('🔍 Filters')

# Area filter
areas = ['All'] + sorted(df['city_area'].unique().tolist())
selected_area = st.sidebar.selectbox('Select Area', areas)

# Restaurant type filter
types = ['All'] + sorted(df['restaurant_type'].dropna().unique().tolist())
selected_type = st.sidebar.selectbox('Restaurant Type', types)

# Price category filter
prices = ['All'] + ['Budget', 'Mid-Range', 'Premium', 'Luxury']
selected_price = st.sidebar.selectbox('Price Category', prices)

# Online order filter
online = st.sidebar.radio('Online Order', ['All', 'Yes', 'No'])

# ---- Apply Filters ----
filtered = df.copy()
if selected_area != 'All':
    filtered = filtered[filtered['city_area'] == selected_area]
if selected_type != 'All':
    filtered = filtered[filtered['restaurant_type'] == selected_type]
if selected_price != 'All':
    filtered = filtered[filtered['price_category'] == selected_price]
if online == 'Yes':
    filtered = filtered[filtered['online_order'] == True]
elif online == 'No':
    filtered = filtered[filtered['online_order'] == False]

# ---- Title ----
st.title('🍽️ Zomato Bangalore Analytics Dashboard')
st.markdown('Analyzing 51,000+ restaurants across 30 areas in Bangalore')
st.markdown('---')

# ---- KPI Metrics ----
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Restaurants', f"{len(filtered):,}")
col2.metric('Average Rating', f"{filtered['rating'].mean():.2f} ⭐")
col3.metric('Average Cost (for 2)', f"₹{filtered['cost'].mean():,.0f}")
col4.metric('Online Order %', f"{(filtered['online_order'].sum()/len(filtered)*100):.1f}%")

st.markdown('---')

# ==================== ROW 1: Area & Cuisine ====================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader('📍 Top 15 Areas by Restaurant Count')
    area_data = filtered['city_area'].value_counts().head(15).reset_index()
    area_data.columns = ['Area', 'Count']
    fig_area = px.bar(
        area_data, x='Count', y='Area',
        orientation='h',
        color='Count',
        color_continuous_scale='Blues'
    )
    fig_area.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig_area, use_container_width=True)

with col_right:
    st.subheader('🍜 Top 10 Cuisines by Average Rating')
    cuisine_data = filtered.groupby('primary_cuisine').agg({
        'rating': 'mean',
        'restaurant_name': 'count'
    }).reset_index()
    cuisine_data.columns = ['Cuisine', 'Avg Rating', 'Count']
    cuisine_data = cuisine_data[cuisine_data['Count'] >= 30]
    cuisine_data = cuisine_data.nlargest(10, 'Avg Rating')
    fig_cuisine = px.bar(
        cuisine_data, x='Avg Rating', y='Cuisine',
        orientation='h',
        color='Avg Rating',
        color_continuous_scale='RdYlGn'
    )
    fig_cuisine.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig_cuisine, use_container_width=True)

# ==================== ROW 2: Ratings & Cost ====================
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader('⭐ Rating Distribution')
    rating_dist = filtered['rating'].round(1).value_counts().sort_index().reset_index()
    rating_dist.columns = ['Rating', 'Count']
    fig_rating = px.bar(
        rating_dist, x='Rating', y='Count',
        color='Rating',
        color_continuous_scale='RdYlGn'
    )
    fig_rating.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_rating, use_container_width=True)

with col_right2:
    st.subheader('💰 Price Category Comparison')
    price_data = filtered.groupby('price_category').agg({
        'rating': 'mean',
        'restaurant_name': 'count',
        'votes': 'mean'
    }).reset_index()
    price_data.columns = ['Price Category', 'Avg Rating', 'Restaurant Count', 'Avg Votes']
    price_data = price_data.dropna()
    fig_price = px.bar(
        price_data, x='Price Category', y='Avg Rating',
        color='Restaurant Count',
        color_continuous_scale='Blues',
        text='Avg Rating'
    )
    fig_price.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_price.update_layout(height=400)
    st.plotly_chart(fig_price, use_container_width=True)

# ==================== ROW 3: Online Order & Restaurant Type ====================
col_left3, col_right3 = st.columns(2)

with col_left3:
    st.subheader('📱 Online Order: Rating Comparison')
    online_data = filtered.groupby('online_order').agg({
        'rating': 'mean',
        'votes': 'mean',
        'restaurant_name': 'count'
    }).reset_index()
    online_data['online_order'] = online_data['online_order'].map({True: 'Online Available', False: 'No Online Order'})
    online_data.columns = ['Order Type', 'Avg Rating', 'Avg Votes', 'Count']
    fig_online = px.bar(
        online_data, x='Order Type', y='Avg Rating',
        color='Order Type',
        color_discrete_sequence=['#2ecc71', '#e74c3c'],
        text='Avg Rating'
    )
    fig_online.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_online.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_online, use_container_width=True)

with col_right3:
    st.subheader('🏪 Top Restaurant Types by Rating')
    type_data = filtered.groupby('restaurant_type').agg({
        'rating': 'mean',
        'restaurant_name': 'count'
    }).reset_index()
    type_data.columns = ['Type', 'Avg Rating', 'Count']
    type_data = type_data[type_data['Count'] >= 20]
    type_data = type_data.nlargest(10, 'Avg Rating')
    fig_type = px.bar(
        type_data, x='Avg Rating', y='Type',
        orientation='h',
        color='Avg Rating',
        color_continuous_scale='Viridis'
    )
    fig_type.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_type, use_container_width=True)

# ==================== ROW 4: Book Table Impact ====================
st.subheader('📊 Book Table Impact on Ratings (Key Finding)')
col_b1, col_b2 = st.columns(2)

with col_b1:
    book_data = filtered.groupby('book_table').agg({
        'rating': 'mean',
        'cost': 'mean',
        'votes': 'mean',
        'restaurant_name': 'count'
    }).reset_index()
    book_data['book_table'] = book_data['book_table'].map({True: 'Table Booking', False: 'No Booking'})
    book_data.columns = ['Booking', 'Avg Rating', 'Avg Cost', 'Avg Votes', 'Count']
    fig_book = px.bar(
        book_data, x='Booking', y='Avg Rating',
        color='Booking',
        color_discrete_sequence=['#3498db', '#95a5a6'],
        text='Avg Rating'
    )
    fig_book.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_book.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_book, use_container_width=True)

with col_b2:
    st.markdown("### Statistical Evidence")
    st.markdown("""
    - **Table booking restaurants: 4.13 avg rating**
    - **No booking restaurants: 3.64 avg rating**
    - **Difference: 0.49 stars** (statistically significant, p < 0.001)
    - This is the strongest predictor of restaurant quality in the dataset
    - Restaurants with table booking also have **3x more votes** on average
    """)

# ==================== KEY INSIGHTS ====================
st.markdown('---')
st.subheader('💡 Key Insights')
st.markdown("""
1. **Table booking is the #1 quality signal** — Restaurants with table booking 
   rate 0.5 stars higher (4.13 vs 3.64). This is statistically significant (p < 0.001).
2. **Modern Indian cuisine leads ratings** at 4.29/5, followed by European (4.22) 
   and Mediterranean (4.17) — all in the premium price range.
3. **BTM has the most restaurants** (3,276) but Church Street and MG Road 
   have the highest average ratings (3.79).
4. **Price correlates moderately with quality** (r = 0.36) — Luxury restaurants 
   average 4.12 vs Budget at 3.62.
5. **Online ordering restaurants** get 22% more customer votes, suggesting 
   higher engagement and visibility.
""")

# ---- Footer ----
st.markdown('---')
st.markdown(
    'Built by **Giriraj Kudupudi** | '
    '[GitHub](https://github.com/GirirajKudupudi) | '
    '[LinkedIn](https://linkedin.com/in/yourprofile)'
)