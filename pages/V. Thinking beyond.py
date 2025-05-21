import streamlit as st
import pandas as pd
import random
import requests

# Set page config FIRST, before any other Streamlit commands
st.set_page_config(page_title="Write your own sentence!", layout="wide")

st.title("Write your own sentence!")

# Define tabs
tab1, tab2, tab3 = st.tabs(["Get a Random Word", "Grammar Check", "The Epic Conclusion"])

# --- TAB 1: Random Word ---
with tab1:
    CSV_URL = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"
    
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

# --- TAB 2: Grammar Check ---
with tab2:
    sentence = st.text_area("Enter your text to check:", height=150)
    
    if st.button("Check Grammar"):
        if sentence.strip():
            url = "https://api.languagetool.org/v2/check"
            data = {'text': sentence, 'language': 'en-US'}
            
            try:
                response = requests.post(url, data=data)
                response.raise_for_status()
                result = response.json()
                
                matches = result.get('matches', [])
                if not matches:
                    st.success("✅ No issues found!")
                else:
                    st.error(f"❌ Found {len(matches)} issue(s):")
                    for i, match in enumerate(matches, 1):
                        context = match.get('context', {})
                        offset = context.get('offset', 0)
                        length = context.get('length', 0)
                        context_text = context.get('text', '')
                        error_part = context_text[offset:offset+length] if context_text else ''
                        
                        replacements = match.get('replacements', [])
                        suggestion = ', '.join([r['value'] for r in replacements]) if replacements else 'No suggestion'
                        
                        st.markdown(
                            f"**Issue {i}:** {match.get('message', 'Unknown error')}\n\n"
                            f"- **Error:** `{error_part}`\n"
                            f"- **Suggestion:** `{suggestion}`\n"
                            f"- **Rule:** {match.get('rule', {}).get('description', 'Unknown rule')}\n"
                        )
            except Exception as e:
                st.error(f"API Error: {str(e)}")
        else:
            st.warning("Please enter some text.")

# --- TAB
