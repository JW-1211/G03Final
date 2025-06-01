import streamlit as st
import pandas as pd
import random
import requests
from gtts import gTTS
from io import BytesIO
import streamlit.components.v1 as components

st.set_page_config(page_title="V. Thinking beyond")
st.title("Get creative!")

tab1, tab2, tab3 = st.tabs([
    "✨1. Creative writing", 
    "📌 Padlet", 
    "✨2. Follow-up activities"
])

# --- TAB 1: Combined Grammar Check & Final Draft ---
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

    st.header("2. Write, Check, and Save Your Story")
    st.markdown(
        "Write a sentence or paragraph about what you think happened next in the story, after Emma went home. "
        "Use one of the random word suggestions by pressing the button above, and make sure to apply the past tense. "
        "You can check your grammar, save your draft, and generate audio for pronunciation practice!"
    )

    if "final_draft" not in st.session_state:
        st.session_state["final_draft"] = ""
    if "audio_data" not in st.session_state:
        st.session_state["audio_data"] = None
    if "grammar_feedback" not in st.session_state:
        st.session_state["grammar_feedback"] = None

    user_text = st.text_area(
        "Write your story here:",
        value=st.session_state["final_draft"],
        height=200,
        key="story_area"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Check Grammar"):
            if user_text.strip():
                url = "https://api.languagetool.org/v2/check"
                data = {'text': user_text, 'language': 'en-US'}
                try:
                    response = requests.post(url, data=data)
                    response.raise_for_status()
                    result = response.json()
                    matches = result.get('matches', [])
                    if not matches:
                        st.session_state["grammar_feedback"] = "✅ There are no grammatical errors found in your writing!"
                    else:
                        feedback = f"❌ Found {len(matches)} issue(s):\n"
                        for i, match in enumerate(matches, 1):
                            context = match.get('context', {})
                            offset = context.get('offset', 0)
                            length = context.get('length', 0)
                            context_text = context.get('text', '')
                            error_part = context_text[offset:offset+length] if context_text else ''
                            replacements = match.get('replacements', [])
                            suggestion = ', '.join([r['value'] for r in replacements]) if replacements else 'No suggestion'
                            feedback += (
                                f"\n**Issue {i}:** {match.get('message', 'Unknown error')}\n"
                                f"- **Error:** `{error_part}`\n"
                                f"- **Suggestion:** `{suggestion}`\n"
                                f"- **Rule:** {match.get('rule', {}).get('description', 'Unknown rule')}\n"
                            )
                        st.session_state["grammar_feedback"] = feedback
                except Exception as e:
                    st.session_state["grammar_feedback"] = f"API Error: {str(e)}"
            else:
                st.session_state["grammar_feedback"] = "Please enter some text."

    with col2:
        if st.button("Save Draft & Generate Audio"):
            st.session_state["final_draft"] = user_text
            if user_text.strip():
                try:
                    tts = gTTS(user_text)
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.session_state["audio_data"] = audio_bytes.read()
                    st.success("Draft saved and audio generated!")
                except Exception as e:
                    st.error(f"Error generating audio: {str(e)}")
            else:
                st.warning("Please write something first!")

    # Show grammar feedback if available (only one message at a time)
    feedback = st.session_state.get("grammar_feedback")
    if feedback:
        if feedback.startswith("✅"):
            st.success(feedback)
        else:
            st.error(feedback)

    # Show latest saved draft and audio if available
    if st.session_state["final_draft"]:
        st.subheader("Your saved draft:")
        st.info(st.session_state["final_draft"])
        if st.session_state.get("audio_data"):
            st.audio(BytesIO(st.session_state["audio_data"]), format="audio/mp3")

# --- TAB 2: Padlet ---
with tab2:
    st.header("📌 Upload your writing to Padlet")
    st.markdown("Share the sentence that you've written with the rest of the class, and work with your teammates to write a paragraph using your assigned words! Visit the Padlet webpage for additional instructions.")
    
    components.iframe(
        "https://padlet.com/thelightside/sentences2go",
        height=600,
        scrolling=True
    )

# --- TAB 3: The Epic Conclusion (restored original content) ---
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
