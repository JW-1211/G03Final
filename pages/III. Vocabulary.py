import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests

# --- Helper: Get synonyms/antonyms from API Ninjas ---
def get_word_relations(word):
    try:
        response = requests.get(
            f"https://api.api-ninjas.com/v1/thesaurus?word={word}",
            headers={'X-Api-Key': st.secrets["API_NINJAS_KEY"]}
        )
        response.raise_for_status()
        data = response.json()
        return {
            'synonyms': data.get('synonyms', []),
            'antonyms': data.get('antonyms', [])
        }
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return {'synonyms': [], 'antonyms': []}

st.write("Vocabulary learning")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💖 1. Lesson: Word list",
    "💖 2. Activity: Listen to the word",
    "💖 3. Spelling practice",
    "💖 4. Word relationships",
    "💖 5. Synonym/Antonym quiz"
])

# --------- TAB 1 ---------
with tab1:
    st.markdown("### 📋 Word Table")
    url = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"
    df = pd.read_csv(url)
    if st.button("Show Word List"):
        st.dataframe(df, use_container_width=True)

# --------- TAB 2 ---------
with tab2:
    st.title("🔊 Word Pronunciation Practice")
    url = "https://raw.githubusercontent
