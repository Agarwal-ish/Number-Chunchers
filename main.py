import pandas as pd 
import streamlit as st
import Preprocessor 
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit App Header
st.set_page_config(page_title="Crime Analysis Dashboard", page_icon="🔍")
st.image("crime.webp", width=130, use_column_width=False) 
st.title("🔍 Crime Analysis Dashboard")
st.subheader("Analyze and visualize crime data to uncover insights.")
st.write("---")
