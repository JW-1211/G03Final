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
        "Write a sentence about what you think happened next in the story, after Emma went home. "
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
                    st.success("✅ There are no grammatical errors found in your writing!")
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
                        
                        st.markdown(f"""**Issue {i}:** {match.get('message', 'Unknown error')}\n
- **Error:** `{error_part}`
- **Suggestion:** `{suggestion}`
- **Rule:** {match.get('rule', {}).get('description', 'Unknown rule')}
""")
            except Exception as e:
                st.error(f"API Error: {str(e)}")
        else:
            st.warning("Please enter some text.")

# --- TAB 2: Padlet + Final Draft ---

with tab2:
    st.header("📌 Upload your writing to Padlet")
    st.markdown("Share the sentence that you've written with the rest of the class, and work with your teammates to write a paragraph by making use of the words that you've been assigned! Visit the Padlet webpage for additional instructions.")

    PADLET_EMBED_URL = "https://padlet.com/thelightside/sentences2go"
    components.iframe(
        PADLET_EMBED_URL,
        height=600,
        scrolling=True
    )

    st.divider()

    # --- Final Draft Section with TTS (moved here) ---
    st.header("3. Final Draft")
    st.markdown("Edit and save your final version of the story here. You can come back and revise it as much as you don't refresh the page! When you're done editing, use the button on the bottom right to generate audio, so that you can practice your pronunciation before sharing your story with the class.")

    if "final_draft" not in st.session_state:
        st.session_state["final_draft"] = ""

    final_draft = st.text_area(
        "Your draft goes here:",
        value=st.session_state["final_draft"],
        height=200,
        key="final_draft_area"
    )

    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("Save Current Draft"):
            st.session_state["final_draft"] = final_draft
            st.success("Draft saved for this session!")
    
    with col2:
        if st.button("🎧 Generate TTS Audio"):
            if final_draft.strip():
                try:
                    tts = gTTS(final_draft)
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as e:
                    st.error(f"Error generating audio: {str(e)}")
            else:
                st.warning("Please write something first!")

    if st.session_state["final_draft"]:
        st.subheader("Your saved draft:")
        st.info(st.session_state["final_draft"])

# --- TAB 3: The Epic Conclusion ---
with tab3:
    st.header("📊 Share your writing with your classmates!")
    st.subheader("Things to keep in mind while presenting:")

    st.markdown("""
    - 1. As you share your story, also explain your reasoning behind it! Describe why you think this might have happened.
    - 2. What are some notable events in your story? Make sure to put in emphasis when you get to the important part.
    - 3. Last but not least - after you've finished sharing, don't forget to ask for peer feedback from your classmates! Brainstorming as a group is a great way to enhance creativity, and make sure that you haven't left any mistakes lying around.
    """)

    st.success("Congratulations! Mission accomplished successfully - congrats on meeting your objectives.")

    st.image(
        "https://raw.githubusercontent.com/JW-1211/G03Final/main/images/story03.png",
        caption="Thank you for participating! :D",
        use_container_width=True
    )
