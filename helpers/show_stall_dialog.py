import streamlit as st
from annotated_text import annotated_text
from helpers.merge_sort import merge_sort

@st.experimental_dialog(f"Stall Details", width="large")
def show_stall_dialog(stall_id, stall_name, stall_rating, stall_tags, stall_lowest_price, stall_highest_price, item_info_df):
    # Filter item_info_df by stall id to show available items and convert to dict
    menu_df = item_info_df[item_info_df['stall_id'] == stall_id]
    menu_df['price'] = menu_df['price'].astype('int')
    
    # Create list of tags
    tag_list = [item.strip() for item in stall_tags.split(',')]
    annotated_items = []
    for tag in tag_list:
        annotated_items.append((tag, ""))
        annotated_items.append(" ")
        
    header_cols = st.columns([0.9, 0.1])
    
    with header_cols[0]:
        annotated_text(*annotated_items)
    with header_cols[1]:
        st.write(f"⭐ {stall_rating}")
          
    st.write(f"**Price Range:** ₱{stall_lowest_price} - ₱{stall_highest_price}")


    cols = st.columns([0.2, 0.5, 0.3],gap="medium")
    with cols[0]:
        st.subheader("Menu")
    with cols[2]:
        sort_option = st.selectbox("Sort by:", ["Price: Low to High", "Price: High to Low", "Rating: Low to High", "Rating: High to Low"], label_visibility="collapsed")
    
    if sort_option == "Price: Low to High":
        filtered_df = merge_sort(menu_df, 'price', ascending=True)
    elif sort_option == "Price: High to Low":
        filtered_df = merge_sort(menu_df, 'price', ascending=False)
    elif sort_option == "Rating: Low to High":
        filtered_df = merge_sort(menu_df, 'food_rating', ascending=True)
    elif sort_option == "Rating: High to Low":
        filtered_df = merge_sort(menu_df, 'food_rating', ascending=False)
        
    menu = filtered_df.to_dict(orient='records')
    
    n_cards_per_row = 2
    cols = st.columns(n_cards_per_row)
    for idx, item in enumerate(menu):
        col = cols[idx % n_cards_per_row]
        with col.container(border=True):
            # Strip item name of leading and trailing whitespaces
            item['item_name'] = item['item_name'].strip()
            st.write(f"**{item['item_name']}** - ₱{item['price']}")
            st.write (f"⭐ {item['food_rating']}")
