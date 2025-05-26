import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests

# --- CONFIGURATION ---
API_NINJAS_KEY = "e+bJafR3fh0DLmxfRkUZfg==GEtwBoUf9Y8wAkyI"  # <-- Replace with your API Ninjas key

CSV_URL = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"
API_URL = "https://api.api-ninjas.com/v1/thesaurus"

@st.cache_data
def load_word_list():
    df = pd.read_csv(CSV_URL)
    if 'Frequency' in df.columns:
        df = df.sort_values('Frequency', ascending=False)
    return df

def get_word_relations(word):
    try:
        response = requests.get(
            f"{API_URL}?word={word}",
            headers={'X-Api-Key': API_NINJAS_KEY}
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

df = load_word_list()
word_list = df["Word"].dropna().tolist()

st.write("🌱 Vocabulary learning")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💖 1. Lesson: Word list",
    "💖 2. Connect the word to the passage",
    "💖 3. Activity: Listen to the word",
    "💖 4. Spelling practice",
    "💖 5. Word relationships",
    "💖 6. Synonym Quiz",
    "💖 7. Antonym Quiz"
])

# TAB 1: Word list
with tab1:
    st.markdown("### 📋 Word Frequency Table")
    if st.button("Show Word List"):
        # Check if 'Definition' column exists
        if 'Definition' in df.columns:
            st.dataframe(
                df[['Word', 'Definition', 'Frequency']] if 'Frequency' in df.columns else df[['Word', 'Definition']],
                use_container_width=True,
                column_config={
                    'Word': 'Vocabulary Term',
                    'Definition': st.column_config.TextColumn('Meaning')
                }
            )
        else:
            st.warning("The 'Definition' column was not found in your CSV file. Please check the column name.")

#TAB 2 : Connect the word to the passage
with tab2: 
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
        "possession" : "the compass now her most treasured **possession**.",
    st.title("📚 Word to the Passage")
    selected_word = st.selectbox("Choose a word",[""] + list(word_examples.keys()))
    if selected_word:
        st.markdown(f"**passage** {word_examples[selected_word]}"
                    
# TAB 3: Listen to the word
with tab3:
    st.title("🔊 Word Pronunciation Practice")
    st.markdown("## Select a word to hear its pronunciation")
    selected_word = st.selectbox("Choose a word:", word_list, key="pronunciation")
    if selected_word:
        tts = gTTS(selected_word, lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp, format='audio/mp3')

# TAB 4: Spelling practice
with tab4:
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

# TAB 5: Word relationships
with tab5:
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

# TAB 6: Synonym Quiz
with tab6:
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
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

# TAB 7: Antonym Quiz
with tab7:
    st.title("🔴 Antonym Quiz")

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
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
