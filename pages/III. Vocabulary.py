import streamlit as st
import pandas as pd
import requests
import random

# --- CONFIGURATION ---
CSV_URL = "https://raw.githubusercontent.com/JW-1211/streamlit25/main/word_frequency2.csv"
API_URL = "https://api.api-ninjas.com/v1/thesaurus"
API_NINJAS_KEY = st.secrets["API_NINJAS_KEY"]  # <-- This line uses the secret

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

tab5 = st.tabs(["❄️ 5. Synonym Quiz"])[0]

with tab5:
    st.title("🟢 Synonym Quiz")

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

    if 'quiz_synonym' not in st.session_state or st.session_state['quiz_synonym'] is None:
        st.session_state['quiz_synonym'] = generate_synonym_quiz()
        st.session_state['score_synonym'] = 0
        st.session_state['answered_synonym'] = False

    quiz = st.session_state['quiz_synonym']
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
        if st.session_state['answered_synonym']:
            if st.button("Next Word", key="next_synonym"):
                st.session_state['quiz_synonym'] = generate_synonym_quiz()
                st.session_state['answered_synonym'] = False
                st.experimental_rerun()
