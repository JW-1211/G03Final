import streamlit as st
st.set_page_config(
    page_title="Vocabulary Learning",
    page_icon="🌱",
    layout="centered"
)

import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests

# --- CONFIGURATION ---
CSV_URL = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"
API_URL = "https://api.api-ninjas.com/v1/thesaurus"
API_NINJAS_KEY = "e+bJafR3fh0DLmxfRkUZfg==GEtwBoUf9Y8wAkyI"  # <-- Place your API key here

# --- CACHING ---
@st.cache_data(show_spinner=False)
def load_word_list():
    df = pd.read_csv(CSV_URL)
    if 'Frequency' in df.columns:
        df = df.sort_values('Frequency', ascending=False)
    return df

@st.cache_data(ttl=3600, show_spinner=False)
def get_word_relations(word):
    try:
        response = requests.get(
            f"{API_URL}?word={word}",
            headers={'X-Api-Key': API_NINJAS_KEY}
        )
        response.raise_for_status()
        data = response.json()
        return {
            'synonyms': data.get('synonyms', [])[:5],
            'antonyms': data.get('antonyms', [])[:5]
        }
    except Exception:
        return {'synonyms': [], 'antonyms': []}

# --- DATA ---
df = load_word_list()
word_list = df["Word"].dropna().tolist()
word_examples = {
    "abundant": "The region is abundant in natural resources.",
    "beneficial": "Regular exercise is beneficial to your health.",
    "consequence": "He was prepared to accept the consequences of his decision.",
    "diminish": "The pain will gradually diminish.",
    "emerge": "She emerged from the room with a smile.",
    "fluctuate": "Oil prices have fluctuated wildly in recent weeks.",
    "gratitude": "She expressed her gratitude to the committee for their support.",
    "harsh": "The weather was too harsh for camping.",
    "inevitable": "It was inevitable that there would be job losses.",
    "justify": "How can you justify the expense?",
    # ...add more as needed
}

# --- UI ---
st.write("🌱 Vocabulary learning")
tabs = st.tabs([f"💖 {i+1}. {title}" for i, title in enumerate([
    "Lesson: Word list", "Connect the word to the passage", 
    "Activity: Listen to the word", "Spelling practice",
    "Word relationships", "Synonym Quiz", "Antonym Quiz"
])])

# --- TAB 1: Word list ---
with tabs[0]:
    st.markdown("### 📋 Word Frequency Table")
    if st.button("Show Word List"):
        if 'Definition' in df.columns:
            st.dataframe(
                df[['Word', 'Definition', 'Frequency']] if 'Frequency' in df.columns else df[['Word', 'Definition']],
                use_container_width=True
            )
        else:
            st.warning("Missing 'Definition' column in CSV file")

# --- TAB 2: Connect word to passage ---
with tabs[1]:
    st.title("📚 Word to the Passage")
    selected_word = st.selectbox("Choose a word", [""] + list(word_examples.keys()), key="passage_word")
    if selected_word:
        st.markdown(f"**Passage:** {word_examples[selected_word]}")

# --- TAB 3: Pronunciation ---
with tabs[2]:
    st.title("🔊 Word Pronunciation Practice")
    selected_word = st.selectbox("Choose a word:", word_list, key="pronunciation")
    if selected_word:
        if 'audio_cache' not in st.session_state:
            st.session_state.audio_cache = {}
        if selected_word not in st.session_state.audio_cache:
            tts = gTTS(selected_word, lang='en')
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            st.session_state.audio_cache[selected_word] = audio_fp.getvalue()
        st.audio(st.session_state.audio_cache[selected_word], format='audio/mp3')

# --- TAB 4: Spelling practice ---
with tabs[3]:
    st.markdown("### 🎧 Listen and Type the Word")
    if 'spelling' not in st.session_state:
        st.session_state.spelling = {'current_word': None, 'audio_data': None, 'user_input': '', 'check_clicked': False}
    if st.button("🔊 Let me listen to a word"):
        st.session_state.spelling['current_word'] = random.choice(word_list)
        tts = gTTS(st.session_state.spelling['current_word'], lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        st.session_state.spelling['audio_data'] = audio_fp.getvalue()
        st.session_state.spelling['user_input'] = ''
        st.session_state.spelling['check_clicked'] = False
    if st.session_state.spelling['audio_data']:
        st.audio(st.session_state.spelling['audio_data'], format='audio/mp3')
    st.session_state.spelling['user_input'] = st.text_input(
        "Type the word you heard:",
        value=st.session_state.spelling['user_input']
    )
    if st.button("✅ Check the answer"):
        st.session_state.spelling['check_clicked'] = True
    if st.session_state.spelling['check_clicked'] and st.session_state.spelling['current_word']:
        if st.session_state.spelling['user_input'].strip().lower() == st.session_state.spelling['current_word'].lower():
            st.success("✅ Correct!")
        else:
            st.error("❌ Try again.")

# --- TAB 5: Word relationships ---
with tabs[4]:
    st.markdown("### 🔄 Synonyms and Antonyms")
    selected_word = st.selectbox("Choose a word to explore:", word_list, key="relationships")
    if selected_word:
        relations = get_word_relations(selected_word)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Synonyms (Green)")
            st.write(", ".join(relations['synonyms']) or "No synonyms found")
        with col2:
            st.markdown("#### Antonyms (Red)")
            st.write(", ".join(relations['antonyms']) or "No antonyms found")

# --- QUIZ HELPERS ---
def generate_quiz(quiz_type):
    eligible = []
    target_key = 'synonyms' if quiz_type == 'synonym' else 'antonyms'
    distractor_key = 'antonyms' if quiz_type == 'synonym' else 'synonyms'
    for word in word_list:
        relations = get_word_relations(word)
        if len(relations[target_key]) >= 1 and len(relations[distractor_key]) >= 3:
            eligible.append((word, relations))
    if eligible:
        word, relations = random.choice(eligible)
        correct = random.choice(relations[target_key])
        distractors = random.sample(relations[distractor_key], 3)
        return {
            'word': word,
            'question': f"Which of the following is a {quiz_type} of '{word}'?",
            'options': random.sample([correct] + distractors, 4),
            'correct': correct
        }
    return None

# --- TAB 6: Synonym Quiz ---
with tabs[5]:
    st.title("🟢 Synonym Quiz")
    if 'synonym_quiz' not in st.session_state:
        st.session_state.synonym_quiz = {'quiz': None, 'score': 0, 'answered': False}
    if st.session_state.synonym_quiz['quiz'] is None:
        st.session_state.synonym_quiz['quiz'] = generate_quiz('synonym')
    quiz = st.session_state.synonym_quiz['quiz']
    if quiz:
        st.markdown(f"### {quiz['question']}")
        selected = st.radio("Options:", quiz['options'], key="options_synonym")
        if st.button("Check Answer", key="check_synonym"):
            st.session_state.synonym_quiz['answered'] = True
            if selected == quiz['correct']:
                st.success("✅ Correct! Well done!")
                st.session_state.synonym_quiz['score'] += 1
            else:
                st.error(f"❌ Incorrect. The correct answer was: {quiz['correct']}")
            st.markdown(f"**Score:** {st.session_state.synonym_quiz['score']}")
        if st.session_state.synonym_quiz['answered'] and st.button("Next Word"):
            st.session_state.synonym_quiz['quiz'] = generate_quiz('synonym')
            st.session_state.synonym_quiz['answered'] = False
            st.rerun()

# --- TAB 7: Antonym Quiz ---
with tabs[6]:
    st.title("🔴 Antonym Quiz")
    if 'antonym_quiz' not in st.session_state:
        st.session_state.antonym_quiz = {'quiz': None, 'score': 0, 'answered': False}
    if st.session_state.antonym_quiz['quiz'] is None:
        st.session_state.antonym_quiz['quiz'] = generate_quiz('antonym')
    quiz = st.session_state.antonym_quiz['quiz']
    if quiz:
        st.markdown(f"### {quiz['question']}")
        selected = st.radio("Options:", quiz['options'], key="options_antonym")
        if st.button("Check Answer", key="check_antonym"):
            st.session_state.antonym_quiz['answered'] = True
            if selected == quiz['correct']:
                st.success("✅ Correct! Well done!")
                st.session_state.antonym_quiz['score'] += 1
            else:
                st.error(f"❌ Incorrect. The correct answer was: {quiz['correct']}")
            st.markdown(f"**Score:** {st.session_state.antonym_quiz['score']}")
        if st.session_state.antonym_quiz['answered'] and st.button("Next Word"):
            st.session_state.antonym_quiz['quiz'] = generate_quiz('antonym')
            st.session_state.antonym_quiz['answered'] = False
            st.rerun()
