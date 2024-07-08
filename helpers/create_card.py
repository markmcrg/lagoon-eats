import streamlit as st
from helpers.show_stall_dialog import show_stall_dialog

def create_card(stall_id, stall_name, lowest_price, highest_price, opening_time, closing_time, days_closed, tags, stall_img_url, rating, item_info_df):
    card = st.container(border=True)
    with card:
        st.image(stall_img_url, use_column_width=True)
        st.write(f"**{stall_name}**")
        st.caption(f"⭐ {rating}")
        st.caption(f"**Stall No:** {stall_id}")
        st.caption(f"**Price Range:** ₱{lowest_price} - ₱{highest_price}")
        st.caption(f"**Opening Hours:** {opening_time} - {closing_time}")
        st.caption(f"**Days Closed:** {days_closed}")
        st.caption(f"**Tags:** {tags}")
        
        if st.button("View Details", key=stall_name):
            show_stall_dialog(stall_id, stall_name, rating, tags, lowest_price, highest_price, item_info_df)