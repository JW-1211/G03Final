import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests
import random

# --- CONFIGURATION ---
api_key = st.secrets["API_NINJAS_KEY"]# <-- Replace with your API Ninjas key
CSV_URL = "https://raw.githubusercontent.com/JW-1211/streamlit25/main/word_frequency2.csv"
API_URL = "https://api.api-ninjas.com/v1/thesaurus"
API_NINJAS_KEY = st.secrets["API_NINJAS_KEY"]  # <-- This line uses the secret

@st.cache_data
def load_word_list():
@@ -33,100 +31,10 @@ def get_word_relations(word):
df = load_word_list()
word_list = df["Word"].dropna().tolist()

st.write("🌱 Vocabulary learning")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "❄️ 1. Lesson: Word list",
    "❄️ 2. Activity: Listen to the word",
    "❄️ 3. Spelling practice",
    "❄️ 4. Word relationships",
    "❄️ 5. Synonym Quiz",
    "❄️ 6. Antonym Quiz"
])

# TAB 1: Word list
with tab1:
    st.markdown("### 📋 Word Frequency Table")
    if st.button("Show Word List"):
        st.dataframe(df, use_container_width=True)

# TAB 2: Listen to the word
with tab2:
    st.title("🔊 Word Pronunciation Practice")
    st.markdown("## Select a word to hear its pronunciation")
    selected_word = st.selectbox("Choose a word:", word_list, key="pronunciation")
    if selected_word:
        tts = gTTS(selected_word, lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp, format='audio/mp3')

# TAB 3: Spelling practice
with tab3:
    st.markdown("### 🎧 Listen and Type the Word")
    st.caption("Click the button to hear a word. Then type it and press 'Check the answer'.")
    if "current_word" not in st.session_state:
        st.session_state.current_word = None
    if "audio_data" not in st.session_state:
        st.session_state.audio_data = None
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "check_clicked" not in st.session_state:
        st.session_state.check_clicked = False

    if st.button("🔊 Let me listen to a word"):
        st.session_state.current_word = random.choice(word_list)
        st.session_state.user_input = ""
        st.session_state.check_clicked = False
        tts = gTTS(st.session_state.current_word, lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.session_state.audio_data = audio_fp.read()

    if st.session_state.audio_data:
        st.audio(st.session_state.audio_data, format='audio/mp3')

    st.session_state.user_input = st.text_input(
        "Type the word you heard:", value=st.session_state.user_input
    )
tab5 = st.tabs(["❄️ 5. Synonym Quiz"])[0]

    if st.button("✅ Check the answer"):
        st.session_state.check_clicked = True

    if st.session_state.check_clicked and st.session_state.current_word:
        if st.session_state.user_input.strip().lower() == st.session_state.current_word.lower():
            st.success("✅ Correct!")
        else:
            st.error("❌ Try again.")

# TAB 4: Word relationships
with tab4:
    st.markdown("### 🔄 Synonyms and Antonyms")
    st.caption("Enrich your vocabulary by learning how a single word can be expressed in different ways!")
    selected_word = st.selectbox("Choose a word to explore:", word_list, key="relationships")
    if selected_word:
        relations = get_word_relations(selected_word)
        synonyms = relations['synonyms']
        antonyms = relations['antonyms']

        st.markdown("---")
        st.markdown("<h4 style='color:green;'>Synonyms</h4>", unsafe_allow_html=True)
        if synonyms:
            st.write(", ".join(synonyms))
        else:
            st.write("No synonyms found.")

        st.markdown("<h4 style='color:red; margin-top:20px;'>Antonyms</h4>", unsafe_allow_html=True)
        if antonyms:
            st.write(", ".join(antonyms))
        else:
            st.write("No antonyms found.")

# TAB 5: Synonym Quiz
with tab5:
    st.title("🟢 Synonym quiz")
    st.title("🟢 Synonym Quiz")

    def generate_synonym_quiz():
        for word in word_list:
@@ -167,47 +75,3 @@ def generate_synonym_quiz():
                st.session_state['quiz_synonym'] = generate_synonym_quiz()
                st.session_state['answered_synonym'] = False
                st.experimental_rerun()

# TAB 6: Antonym Quiz
with tab6:
    st.title("🔴 Antonym quiz")

    def generate_antonym_quiz():
        for word in word_list:
            relations = get_word_relations(word)
            if len(relations['antonyms']) >= 1 and len(relations['synonyms']) >= 3:
                correct = random.choice(relations['antonyms'])
                distractors = random.sample(relations['synonyms'], 3)
                options = [correct] + distractors
                random.shuffle(options)
                return {
                    'word': word,
                    'question': f"Which of the following is an antonym of '{word}'?",
                    'options': options,
                    'correct': correct
                }
        st.error("Could not generate an antonym quiz. Try again later.")
        return None

    if 'quiz_antonym' not in st.session_state or st.session_state['quiz_antonym'] is None:
        st.session_state['quiz_antonym'] = generate_antonym_quiz()
        st.session_state['score_antonym'] = 0
        st.session_state['answered_antonym'] = False

    quiz = st.session_state['quiz_antonym']
    if quiz:
        st.markdown(f"### {quiz['question']}")
        selected = st.radio("Options:", quiz['options'], key="options_antonym")
        if st.button("Check Answer", key="check_antonym"):
            st.session_state['answered_antonym'] = True
            if selected == quiz['correct']:
                st.success("✅ Correct! Well done!")
                st.session_state['score_antonym'] += 1
            else:
                st.error(f"❌ Incorrect. The correct answer was: {quiz['correct']}")
            st.markdown(f"**Score:** {st.session_state['score_antonym']}")
        if st.session_state['answered_antonym']:
            if st.button("Next Word", key="next_antonym"):
                st.session_state['quiz_antonym'] = generate_antonym_quiz()
                st.session_state['answered_antonym'] = False
                st.experimental_rerun()
