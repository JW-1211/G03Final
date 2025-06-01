import streamlit as st
import pandas as pd
import random
import requests
from gtts import gTTS
from io import BytesIO
import streamlit.components.v1 as components  # For embedding Padlet

st.set_page_config(page_title="V. Thinking beyond")

st.title("Get creative!")

# Define tabs with Padlet as tab2
tab1, tab2, tab3 = st.tabs([
    "✨1. Creative writing", 
    "📌 Padlet", 
    "✨2. Follow-up activities"
])

# --- TAB 1: Combined Random Word & Grammar Check ---
with tab1:
    st.header("1. Get a Random Word from the Story")
    CSV_URL = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocab_past.csv"
    
    @st.cache_data
    def load_words(url):
        try:
            df = pd.read_csv(url)
            return df
        except Exception as e:
            st.error(f"Error loading CSV: {str(e)}")
            return None
    
    df = load_words(CSV_URL)
    
    if df is not None:
        if "Word" not in df.columns:
            st.error("CSV must have a column named 'Word'.")
        else:
            if st.button("Suggest a Random Word"):
                word = random.choice(df["Word"].dropna().tolist())
                st.success(f"Your random word is: **{word}**")

    st.divider()

    st.header("2. Grammar Checker")
    st.markdown(
