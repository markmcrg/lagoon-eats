import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_searchbox import st_searchbox
from helpers.create_card import create_card
from helpers.merge_sort import merge_sort

st.set_page_config(page_title='Lagoon Eats', page_icon='🍔', layout='wide', initial_sidebar_state='auto')

# Load data from Google Sheets
url = "https://docs.google.com/spreadsheets/d/1oW8ds8_wGrU3HfnYlBvnQwUv9jr_AjxqlpBUndO4G0E/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Load data and set cache to minimize reloading
@st.cache_data(show_spinner="Fetching data...")
def load_data():
    stall_info_df = conn.read(spreadsheet=url, ttl="10m")
    item_info_df = conn.read(spreadsheet=url, ttl="10m", worksheet="1266150423")
    return stall_info_df, item_info_df

stall_info_df, item_info_df = load_data()

# Sidebar filters and options
with st.sidebar:
    st.title('🍔 Lagoon Eats')
    clear_cache = st.button("Clear Cache")
    if clear_cache:
        st.cache_data.clear()
    sort_price = st.radio("Sort By", ("A-Z", "Z-A", "Price: Low to High", "Price: High to Low"))
    
    st.header("Filters")
    # Filter by Price
    price_filter = st.toggle("Filter by Price")
    if price_filter:
        price_range = st.slider("Select Price Range", 5, 300, (30, 100))
    
    # Filter by Rating
    rating_filter = st.toggle("Filter by Rating")
    if rating_filter:
        rating = st.radio("Select Rating", ["⭐ 5.0", "⭐ 4.0 & Up", "⭐ 3.0 & Up", "⭐ 2.0 & Up", "⭐ 1.0 & Up"])
        min_rating = float(rating.split()[1])
    else:
        min_rating = 0
    
    # Filter by Cuisine
    cuisines = [
        "Asian", "Beverages", "Bread", "Burgers", "Chicken", 
        "Coffee", "Desserts", "Filipino", "Fries", "Healthy", 
        "Ice Cream", "Noodles", "Rice Bowl", "Rice Dishes", 
        "Sandwiches", "Shawarma", "Silog", "Siomai", "Snacks", 
        "Soups", "Student Meal"
    ]
    selected_cuisines = st.multiselect("Filter by Cuisine", cuisines)


# Search form
with st.form('search_form'):
    col1, col2 = st.columns([8,1])
    stall_query = col1.text_input("Enter Food Stall Name:", placeholder="Search for a stall...", label_visibility='collapsed')
    submitted = col2.form_submit_button('🔍 Search')    
        
# Filter logic
def filter_stalls(df):
    if stall_query:
        df = df[df['stall_name'].str.contains(stall_query, case=False, na=False)]
    if price_filter:
        df = df[(df['lowest_price'] >= price_range[0]) & (df['highest_price'] <= price_range[1])]
    if rating_filter:
        df = df[df['rating'] >= min_rating]
    if selected_cuisines:
        # Create a regex pattern to match any of the selected cuisines
        pattern = '|'.join(selected_cuisines)
        df = df[df['tags'].str.contains(pattern, case=False, na=False)]
    return df

# Apply filters and sorting
filtered_stalls = filter_stalls(stall_info_df)

# Sorting logic
if sort_price == "A-Z":
    filtered_stalls = merge_sort(filtered_stalls, 'stall_name', ascending=True)
elif sort_price == "Z-A":
    filtered_stalls = merge_sort(filtered_stalls, 'stall_name', ascending=False)
elif sort_price == "Price: Low to High":
    filtered_stalls = merge_sort(filtered_stalls, 'lowest_price', ascending=True)
elif sort_price == "Price: High to Low":
    filtered_stalls = merge_sort(filtered_stalls, 'lowest_price', ascending=False)

# Display stalls in a grid layout
def display_stalls(filtered_stalls):
    try:
        n_cards_per_row = 4
        rows = [filtered_stalls.iloc[i:i + n_cards_per_row] for i in range(0, len(filtered_stalls), n_cards_per_row)]
        for row in rows:
            cols = st.columns(n_cards_per_row)
            for idx, col in enumerate(cols):
                with col:
                    if idx < len(row):
                        stall = row.iloc[idx]
                        # Generate stall info
                        create_card(stall['stall_id'],stall['stall_name'], stall['lowest_price'], stall['highest_price'], stall['opening_time'], stall['closing_time'], stall['days_closed'], stall['tags'], stall['stall_img_url'], stall['rating'], item_info_df)
    except AttributeError:
        pass

display_stalls(filtered_stalls)