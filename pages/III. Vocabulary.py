import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests

CSV_URL = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"
API_URL = "https://api.api-ninjas.com/v1/thesaurus"
API_NINJAS_KEY = "e+bJafR3fh0DLmxfRkUZfg==GEtwBoUf9Y8wAkyI"  # <-- Place your API key here

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

df = load_word_list()
word_list = df["Word"].dropna().tolist()

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

# --- TAB 2: Connect the word to the passage ---
word_examples = {
    "compass" : "Emma found an old **compass** in her attic one rainy afternoon.",
    "journey" : "The **journey** ended at the gallery, where the compass stopped moving.",
    "desire" : "Emma realized her **desire** to become an artist.",
    "attic" : "Emma found an old compass in her **attic** one rainy afternoon.",
    "magnetic" : "It pointed to the one's greatest desire rather than **magnetic** north.",
    "curiosity" : "Emma, driven by **curiosity**, followed the compass's lead.",
    "deserted" : "The compass led her to various places: a lonely old bookstore, a **deserted** park, and finally, a small, forgotten art gallery.",
    "discover" : "At each stop, she **discovered** pieces of her own hidden passions.",
    "passion" : "At each stop, she discovered pieces of her own hidden **passions**.",
    "literature" : "At each stop, she discovered pieces of her own hidden passions: **literature**, nature, and art.",
    "inspire" : "**Inspired**, Emma went home to start her first painting.",
    "treasured" : "The compass now her most **treasured** possession.",
    "possession" : "the compass now her most treasured **possession**."
}  # <-- Fixed: missing closing bracket

with tabs[1]:
    st.title("📚 Word to the Passage")
    selected_word = st.selectbox("Choose a word", [""] + list(word_examples.keys()))
    if selected_word:
        st.markdown(f"**passage** {word_examples[selected_word]}")  # <-- Fixed: missing parenthesis

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
def generate_synonym_quiz():
    for word in word_list:
        relations = get_word_relations(word)
        if len(relations['synonyms']) >= 1 and len(relations['antonyms']) >= 3:
            correct = random.choice(relations['synonyms'])
            distractors = random.sample(relations['antonyms'], 3)
            options = [correct] + distractors
            random.shuffle(options)
            return {
                'word': word,
                'question': f"Which of the following is a synonym of '{word}'?",
                'options': options,
                'correct': correct
            }
    st.error("Could not generate a synonym quiz. Try again later.")
    return None

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

# --- TAB 6: Synonym Quiz ---
with tabs[5]:
    st.title("🟢 Synonym Quiz")
    if 'quiz_synonym' not in st.session_state or st.session_state['quiz_synonym'] is None:
        st.session_state['quiz_synonym'] = generate_synonym_quiz()
        st.session_state['score_synonym'] = 0
        st.session_state['answered_synonym'] = False

    quiz = st.session_state['quiz_synonym']  # <-- Fixed: define quiz
    if quiz:
        st.markdown(f"### {quiz['question']}")
        selected = st.radio("Options:", quiz['options'], key="options_synonym")
        if st.button("Check Answer", key="check_synonym"):
            st.session_state['answered_synonym'] = True
            if selected == quiz['correct']:
                st.success("✅ Correct! Well done!")
                st.session_state['score_synonym'] += 1
            else:
                st.error(f"❌ Incorrect. The correct answer was: {quiz['correct']}")
            st.markdown(f"**Score:** {st.session_state['score_synonym']}")
        if st.session_state['answered_synonym'] and st.button("Next Word"):
            st.session_state['quiz_synonym'] = generate_synonym_quiz()
            st.session_state['answered_synonym'] = False
            st.rerun()

# --- TAB 7: Antonym Quiz ---
with tabs[6]:
    st.title("🔴 Antonym Quiz")
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
        if st.session_state['answered_antonym'] and st.button("Next Word"):
            st.session_state['quiz_antonym'] = generate_antonym_quiz()
            st.session_state['answered_antonym'] = False
            st.rerun()
