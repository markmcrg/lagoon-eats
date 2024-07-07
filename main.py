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
        "Beverages", "Burgers", "Chicken", 
        "Coffee", "Filipino", "Fries", 
        "Ice Cream", "Noodles", "Rice Bowl", 
        "Rice Dishes", "Silog", "Siomai", "Snacks", 
    ]
    selected_cuisines = st.multiselect("Filter by Cuisine", cuisines)

def bad_character_table(pattern: str):
    """ Generates the bad character table. """
    table = {}
    length = len(pattern)
    for i in range(length - 1):
        table[pattern[i]] = length - i - 1
    return table

def boyer_moore_search(text: str, pattern: str):
    """ Performs the Boyer-Moore search algorithm. """
    if not pattern or not text:
        return False
    
    bad_char_table = bad_character_table(pattern)
    m = len(pattern)
    n = len(text)

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return True
        else:
            i += bad_char_table.get(text[i + j], m)
    return False

# Search logic
def search_stall(query: str):
    # Get all stall names from df
    stall_names = stall_info_df['stall_name'].tolist()
    # Loop through all stall names
    result = []
    for stall in stall_names:
        if boyer_moore_search(stall.lower(), query.lower()):
            result.append(stall)
    return result

def show_stall_results(df):
    result = []
    stall_names = df['stall_name'].tolist()
    for stall in stall_names:
        if boyer_moore_search(stall.lower(), stall_query.lower()):
            result.append(stall)
            
    # Return a df with all matching stall names in list
    df = df[df['stall_name'].isin(result)]
    return df

# Search form
with st.container(border=True):
    col1, col2 = st.columns([8,1])
    with col1:
        stall_query = st_searchbox(
            placeholder="Search for a stall...", 
            key='search_query', 
            search_function=search_stall,
            default_use_searchterm=True,
            edit_after_submit="option"
        )  
    with col2:
        submitted = st.button('🔍 Search')    
    
# Filter logic
def filter_stalls(df):
    if stall_query:
        df = show_stall_results(df)
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