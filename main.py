import streamlit as st

st.set_page_config(page_title='Lagoon Eats', page_icon='🍔', layout='wide', initial_sidebar_state='auto')

# Sidebar
with st.sidebar:
    st.title('🍔 Lagoon Eats')
    st.header("Filters")
    
    # Checkbox for sorting by price
    st.subheader("Sort By")
    sort_price = st.radio("Price", ("Low to High", "High to Low"))
    
    # Slider for price range filter
    st.subheader("Price Range")
    price_range = st.slider("Select Price Range", 20, 200, (30, 100)) 
    
    # Radio buttons for selecting rating filter
    st.subheader("Rating")
    rating_filter = st.radio("Select Rating", ("⭐ 5.0", "⭐ 4.0 & Up", "⭐ 3.0 & Up", "⭐ 2.0 & Up", "⭐ 1.0 & Up"))
    
    # Checkbox for selecting cuisine
    st.subheader("Cuisine")
    cuisines = [
    "Asian", "Beverages", "Bread", "Burgers", "Chicken", 
    "Coffee", "Desserts", "Filipino", "Fries", "Healthy", 
    "Ice Cream", "Noodles", "Rice Bowl", "Rice Dishes", 
    "Sandwiches", "Shawarma", "Silog", "Siomai", "Snacks", 
    "Soups", "Student Meal"
    ]
    selected_cuisines = {}
    # Loop through the list and create a checkbox for each item
    for cuisine in cuisines:
        selected_cuisines[cuisine] = st.checkbox(cuisine)
    
    
    
st.text_input("Search for a food stall", placeholder="Type here...")
st.button("Search")

