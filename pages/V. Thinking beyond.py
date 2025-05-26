import streamlit as st
import pandas as pd
import random
import requests

st.set_page_config(page_title="V. Thinking beyond")  # Default centered layout

st.title("Get creative!")

# Define tabs
tab1, tab2 = st.tabs(["Creative writing", "Follow-up activities"])

# --- TAB 1: Combined Random Word & Grammar Check ---
with tab1:
    st.header("1. Get a Random Word")
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
        "Write about what you think happened next in the story, after Emma went home. "
        "Use one of the random word suggestions by pressing the button above, and make sure to apply the past tense. "
        "You'll get instant feedback and suggestions for improving your creative writing!"
    )
    sentence = st.text_area("Enter your story to check for errors:", height=150)
    
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

# --- TAB 2: The Epic Conclusion ---
with tab2:
    st.header("📊 App Conclusion & Summary")
    st.subheader("Key Takeaways")

    st.markdown("""
    **This application:**
    - Allows a easy understanding of paragraphs by utilizing word cloud and illustrations.
    - Provides a thorough analysis of vocabulary and grammar.
    - Helps to take a step beyond simple memorization, and practice application through creative writing.

    """)
    st.success("Congratulations! Your project objectives have been met.")

    st.image(
        "https://raw.githubusercontent.com/JW-1211/G03Final/main/images/diagram%20goes%20here.png",
        caption="The big picture!",
        use_container_width=True
    )

    st.divider()

    st.info("For more details or to discuss results, contact the project team.")
