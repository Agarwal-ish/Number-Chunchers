import pandas as pd
import streamlit as st

# Multiselect fucntion 
def multiselect(title, option_lists):
    selected = st.sidebar.multiselect(title, option_lists)
    select_all = st.sidebar.checkbox("Select All",value = True, key = title)
    if select_all:
        selected_options = option_lists
    else:
        selected_options = selected
    return selected_options
