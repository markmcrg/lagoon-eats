import streamlit as st
from annotated_text import annotated_text

@st.experimental_dialog("Stall Details", width="large")
def show_stall_dialog(stall_id, stall_name, stall_rating, stall_tags, stall_lowest_price, stall_highest_price, item_info_df):
    # Filter item_info_df by stall id to show available items and convert to dict
    menu_df = item_info_df[item_info_df['stall_id'] == stall_id]
    menu_df['price'] = menu_df['price'].astype('int')
    menu = menu_df.to_dict(orient='records')
    
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

    tab1, tab2 = st.tabs(["Menu", "Mix & Match"])
    with tab1:
        st.subheader("Menu")
        n_cards_per_row = 2
        cols = st.columns(n_cards_per_row)
        for idx, item in enumerate(menu):
            col = cols[idx % n_cards_per_row]
            with col.container(border=True):
                st.write(f"**{item['item_name']}** - ₱{item['price']}")
                st.write (f"⭐ {item['food_rating']}")
                
    with tab2:
        st.write("mix and match")