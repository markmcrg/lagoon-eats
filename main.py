from xml.dom.minidom import Attr
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_searchbox import st_searchbox

st.set_page_config(page_title='Lagoon Eats', page_icon='🍔', layout='wide', initial_sidebar_state='auto')

# Load data from Google Sheets
url = "https://docs.google.com/spreadsheets/d/1oW8ds8_wGrU3HfnYlBvnQwUv9jr_AjxqlpBUndO4G0E/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Load data and set cache to minimize reloading
@st.cache_data
def load_data():
    stall_info_df = conn.read(spreadsheet=url, ttl="10m")
    item_info_df = conn.read(spreadsheet=url, ttl="10m", worksheet="1266150423")
    return stall_info_df, item_info_df

stall_info_df, item_info_df  = load_data()

# Sidebar filters and options
with st.sidebar:
    st.title('🍔 Lagoon Eats')
    clear_cache = st.button("Clear Cache")
    if clear_cache:
        st.cache_data.clear()
    sort_price = st.radio("Sort By", ("A-Z", "Z-A", "Low to High", "High to Low"))
    
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
    
def create_card(stall_id, stall_name, lowest_price, highest_price, opening_time, closing_time, days_closed, tags, stall_img_url, promo):
    card = st.container(border=True)
    with card:
        st.image(stall_img_url, use_column_width=True)
        st.write(f"**{stall_name}**")
        st.caption(f"**Price Range:** ₱{lowest_price} - ₱{highest_price}")
        st.caption(f"**Opening Hours:** {opening_time} - {closing_time}")
        st.caption(f"**Days Closed:** {days_closed}")
        st.caption(f"**Tags:** {tags}")
        st.caption(f"**Promo:** {promo}")
        
        if st.button("View Details", key=stall_name):
            stall_dialog(stall_id, stall_name, stall_img_url, "Stall Info", "Item Info", "User Ratings")
        
        
# Filter and sort logic
def filter_sort_stalls(df):
    if stall_query:
        df = df[df['stall_name'].str.contains(stall_query, case=False, na=False)]
    if price_filter:
        df = df[(df['lowest_price'] >= price_range[0]) & (df['highest_price'] <= price_range[1])]
    # if rating_filter:
    #     df = df[df['rating'] >= min_rating]
    if selected_cuisines:
        # Create a regex pattern to match any of the selected cuisines
        pattern = '|'.join(selected_cuisines)
        df = df[df['tags'].str.contains(pattern, case=False, na=False)]
    return df

# Apply filters and sorting
filtered_stalls = filter_sort_stalls(stall_info_df)

# Sorting
if sort_price == "A-Z":
    filtered_stalls.sort_values(by='stall_name', inplace=True)
elif sort_price == "Z-A":
    filtered_stalls.sort_values(by='stall_name', inplace=True, ascending=False)
elif sort_price == "Low to High":
    filtered_stalls.sort_values(by='lowest_price', inplace=True)
elif sort_price == "High to Low":
    filtered_stalls.sort_values(by='lowest_price', inplace=True, ascending=False)

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
                        create_card(stall['stall_id'],stall['stall_name'], stall['lowest_price'], stall['highest_price'], stall['opening_time'], stall['closing_time'], stall['days_closed'], stall['tags'], stall['stall_img_url'], stall['promo'])
    except AttributeError:
        pass

@st.experimental_dialog("Stall Details", width="large")
def stall_dialog(stall_id, stall_name, stall_img_url, stall_info, item_info, user_ratings):
    # Filter item_info_df by stall id to show available items and convert to dict
    menu_df = item_info_df[item_info_df['stall_id'] == stall_id]
    menu_df['price'] = menu_df['price'].astype()
    menu = menu_df.to_dict(orient='records')
    # lowest to highest price
    # rating
    tab1, tab2 = st.tabs(["Menu", "Mix & Match"])
    with tab1:
        st.subheader("Menu")
        n_cards_per_row = 2
        cols = st.columns(n_cards_per_row)
        for idx, item in enumerate(menu):
            col = cols[idx % n_cards_per_row]
            with col.container(border=True):
                st.write(f"**{item['item_name']}** - ₱{item['price']}")
                

    with tab2:
        st.write("mix and match")

display_stalls(filtered_stalls)

# TO ADD:
# Autocomplete search
# make mergesort.py
