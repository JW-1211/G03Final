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
        "possession" : "the compass now her most treasured **possession**."
    }  # <-- Added missing closing brace

    st.title("📚 Word to the Passage")
    selected_word = st.selectbox("Choose a word", [""] + list(word_examples.keys()))
    if selected_word:
        st.markdown(f"**Passage:** {word_examples[selected_word]}")  # <-- Added missing parenthesis

                    
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

# TAB 4: Vocabulary Quiz
with tab4
    st.header("💡 Multiple Choice Vocabulary Quiz")

    vocab_pairs = df[['Word', 'Meaning']].dropna().values.tolist()

    if len(vocab_pairs) < 4:
        st.warning("퀴즈를 만들기 위해 단어가 충분하지 않습니다.")
    else:
        question = random.choice(vocab_pairs)
        word, correct_meaning = question
        wrong_choices = random.sample(
            [m for w, m in vocab_pairs if m != correct_meaning],
            3
        )
        options = wrong_choices + [correct_meaning]
        random.shuffle(options)
        st.subheader(f"🔤 단어: **{word}**")
        user_answer = st.radio(“Choose the right meaning:", options)
        if st.button("Check answer", key="submit_quiz"):
            if user_answer == correct_meaning:
                st.success("✅ Well done!")
            else:
                st.error(f"❌ Error. The right answer is: **{correct_meaning}**")
        if st.button("🔁 Next word", key="next_quiz"):
            st.experimental_rerun()


# TAB 5: Word relationships
with tab5:
    synonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_synonyms.csv")
    antonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_antonyms.csv")
    sentences_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_sentences.csv")

    all_words = sorted(
        set(synonyms_df['word']).union(set(antonyms_df['word']))
    )

    selected_word = st.selectbox("Choose a word (relationships):", all_words, key="relationships")

    def get_word_list(df, word, prefix):
        row = df[df['word'] == word]
        if row.empty:
            return []
        values = []
        for i in range(1, 4):
            val = row[f"{prefix}{i}"].values[0] if f"{prefix}{i}" in row else None
            if pd.notna(val) and val != '':
                values.append(val)
        return values

    synonyms = get_word_list(synonyms_df, selected_word, "synonym")
    antonyms = get_word_list(antonyms_df, selected_word, "antonym")

    # Session state for clicked word
    if "clicked_word" not in st.session_state:
        st.session_state.clicked_word = None
    if "clicked_type" not in st.session_state:
        st.session_state.clicked_type = None

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Synonyms")
        if synonyms:
            for syn in synonyms:
                cols = st.columns([3, 2])
                if cols[0].button(syn, key=f"syn_{syn}"):
                    st.session_state.clicked_word = syn
                    st.session_state.clicked_type = "synonym"
                # Generate audio for the synonym
                tts = gTTS(syn, lang='en')
                audio_fp = BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                with cols[1]:
                    st.audio(audio_fp, format='audio/mp3')
        else:
            st.info("This word doesn't have any matching synonyms.")

    with col2:
        st.subheader("Antonyms")
        if antonyms:
            for ant in antonyms:
                cols = st.columns([3, 2])
                if cols[0].button(ant, key=f"ant_{ant}"):
                    st.session_state.clicked_word = ant
                    st.session_state.clicked_type = "antonym"
                # Generate audio for the antonym
                tts = gTTS(ant, lang='en')
                audio_fp = BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                with cols[1]:
                    st.audio(audio_fp, format='audio/mp3')
        else:
            st.info("This word doesn't have any matching antonyms.")

    st.divider()
    # Only display something if a word has been clicked
    if st.session_state.clicked_word:
        row = sentences_df[
            (sentences_df['word'] == selected_word) &
            (sentences_df['related_word'] == st.session_state.clicked_word)
        ]
        sentences_found = False
        if not row.empty:
            for i in range(1, 4):
                col = f"sentence{i}"
                sentence = row.iloc[0][col] if col in row.columns else None
                if pd.notna(sentence) and sentence != '':
                    sentences_found = True
                    sent_cols = st.columns([6, 2])
                    sent_cols[0].write(f"**Example sentence:** {sentence}")
                    tts = gTTS(sentence, lang='en')
                    audio_fp = BytesIO()
                    tts.write_to_fp(audio_fp)
                    audio_fp.seek(0)
                    with sent_cols[1]:
                        st.audio(audio_fp, format='audio/mp3')
        # Only show the message if a word was clicked and there are truly no sentences
        if not sentences_found:
            pass  # Show nothing

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

    quiz = st.session_state['quiz_synonym']  # <-- Properly define quiz
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
                st.rerun()


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
