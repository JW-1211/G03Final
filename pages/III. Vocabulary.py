import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests

# --- CONFIGURATION ---
API_NINJAS_KEY = "e+bJafR3fh0DLmxfRkUZfg==GEtwBoUf9Y8wAkyI"
CSV_URL = "https://raw.githubusercontent.com/JW-1211/streamlit25/refs/heads/main/word_frequency2.csv"
API_URL = "https://api.api-ninjas.com/v1/thesaurus"

@st.cache_data
def load_word_list():
    df = pd.read_csv(CSV_URL)
    if 'Frequency' in df.columns:
        df = df.sort_values('Frequency', ascending=False)
    return df

def get_word_relations(word):
    try:
        response = requests.get(f"{API_URL}?word={word}", headers={'X-Api-Key': API_NINJAS_KEY})
        response.raise_for_status()
        data = response.json()
        return {
            'synonyms': data.get('synonyms', []),
            'antonyms': data.get('antonyms', [])
        }
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return {'synonyms': [], 'antonyms': []}

df = load_word_list()
word_list = df["Word"].dropna().tolist()

st.write("🌱 Vocabulary learning")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "❄️ 1. Lesson: Word list",
    "❄️ 2. Activity: Listen to the word",
    "❄️ 3. Spelling practice",
    "❄️ 4. Word relationships",
    "❄️ 5. Check your understanding"
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

# TAB 5: Antonym quiz
with tab5:
    st.title("Antonym Quiz Challenge 🔄")

    def generate_quiz_question():
        for word in word_list:
            relations = get_word_relations(word)
            if len(relations['antonyms']) >= 1 and len(relations['synonyms']) >= 3:
                correct_answer = random.choice(relations['antonyms'])
                distractors = random.sample(relations['synonyms'], 3)
                options = [correct_answer] + distractors
                random.shuffle(options)
                return {
                    'question': f"Which of the following is an antonym of '{word}'?",
                    'options': options,
                    'correct': correct_answer,
                    'word': word
                }
        st.error("Could not generate quiz questions. Some words may lack sufficient synonyms/antonyms.")
        return None

    if 'current_question' not in st.session_state:
        st.session_state.current_question = generate_quiz_question()
        st.session_state.score = 0
        st.session_state.show_answer = False

    q = st.session_state.current_question
    if q:
        st.markdown(f"### {q['question']}")
        selected = st.radio("Options:", q['options'], key="antonym_quiz_options")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Check Answer", key="antonym_check"):
                st.session_state.show_answer = True

        if st.session_state.show_answer:
            if selected == q['correct']:
                st.success("✅ Correct! Well done!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Incorrect. The correct antonym was: {q['correct']}")
            st.markdown(f"**Current Score:** {st.session_state.score}")
            if st.button("Next Question", key="antonym_next"):
                st.session_state.current_question = generate_quiz_question()
                st.session_state.show_answer = False
                st.experimental_rerun()
