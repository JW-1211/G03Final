import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests

st.markdown("""
    <style>
    /* Make the Streamlit tab bar horizontally scrollable */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        white-space: nowrap !important;
        display: flex !important;
        scrollbar-width: thin;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 0 0 auto !important;
    }
    </style>
""", unsafe_allow_html=True)


CSV_URL = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"

@st.cache_data
def load_word_list():
    df = pd.read_csv(CSV_URL)
    if 'Frequency' in df.columns:
        df = df.sort_values('Frequency', ascending=False)
    return df



df = load_word_list()
word_list = df["Word"].dropna().tolist()

st.title("🌱 Vocabulary learning")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🐥 1. Lesson: Word list",
    "📚 2. Connect the word to the passage",
    "🔉 3. Activity: Listen to the word",
    "✅ 4. Vocabulary Quiz",
    "🔗 5. Word relations",
    "💖 6. Relations quiz"
])

# TAB 1: Word list
with tab1:
    st.markdown("### 📋 Word List")
    if st.button("Show Word List"):
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

    if st.button("Show Easy Word List"):
        st.markdown("#### 🔹 Word List from GitHub")
        csv_url = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/voc.csv#L8"
        try:
            df_remote = pd.read_csv(csv_url)

            if 'Definition' in df_remote.columns:
                st.dataframe(
                    df_remote[['Word', 'Definition', 'Frequency']] if 'Frequency' in df_remote.columns else df_remote[['Word', 'Definition']],
                    use_container_width=True,
                    column_config={
                        'Word': 'Vocabulary Term',
                        'Definition': st.column_config.TextColumn('Meaning')
                    }
                )
            else:
            
                st.warning("The 'Definition' column was not found in the GitHub CSV.")
        except Exception as e:
            st.error(f"Error loading data from GitHub: {e}")
            
            

# TAB 2 : Connect the word to the passage
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
    }
    st.title("📚 Word to the Passage")
    selected_word = st.selectbox("Choose a word", [""] + list(word_examples.keys()))
    if selected_word:
        st.markdown(f"**Passage:** {word_examples[selected_word]}")

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
with tab4:
    st.header("💡 Multiple Choice Vocabulary Quiz")

    if "Word" not in df.columns or "Definition" not in df.columns:
        st.error("❌ The CSV file must contain 'Word' and 'Definition' columns.")
        st.stop()

    vocab_pairs = df[['Word', 'Definition']].dropna().values.tolist()
    cleaned_pairs = []
    for word, definition in vocab_pairs:
        main_meaning = definition.split(')')[0] + ')' if ')' in definition else definition
        cleaned_pairs.append((word.strip(), main_meaning.strip()))

    cleaned_pairs = list(set(cleaned_pairs))

    if len(cleaned_pairs) < 4:
        st.warning("⚠️ Not enough vocabulary data to run the quiz.")
    else:
        if "quiz_data" not in st.session_state:
            question = random.choice(cleaned_pairs)
            word, correct_def = question
            wrong_defs = [d for w, d in cleaned_pairs if d != correct_def]
            wrong_choices = random.sample(wrong_defs, 3)
            options = wrong_choices + [correct_def]
            random.shuffle(options)

            st.session_state.quiz_data = {
                "word": word,
                "correct": correct_def,
                "options": options,
                "answered": False
            }

        q = st.session_state.quiz_data

        st.subheader(f"📖 What is the meaning of the word: **{q['word']}**?")
        user_choice = st.radio("Select the correct definition:", q['options'], key="quiz_choice")

        if st.button("Submit") and not q["answered"]:
            if user_choice == q["correct"]:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong. The correct answer is: **{q['correct']}**")
            st.session_state.quiz_data["answered"] = True

        if q["answered"]:
            if st.button("Next Question"):
                del st.session_state.quiz_data
                st.rerun()  # Use st.rerun() instead of return

# TAB 5: Word relationships
with tab5:
    st.markdown("""
    <style>
    hr {
        margin-top: 0.1rem !important;
        margin-bottom: 0.1rem !important;
    }
    [data-testid="stCaption"] {
        margin-top: 0.1rem !important;
        margin-bottom: 0.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

with tab5:
    synonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_synonyms.csv")
    antonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_antonyms.csv")
    sentences_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_sentences.csv")

    all_words = sorted(
        set(synonyms_df['word']).union(set(antonyms_df['word']))
    )

    selected_word = st.selectbox("Choose a word:", all_words, key="relationships")

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
                tts = gTTS(ant, lang='en')
                audio_fp = BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                with cols[1]:
                    st.audio(audio_fp, format='audio/mp3')
        else:
            st.info("This word doesn't have any matching antonyms.")

    # --- Caption just above the divider, with minimal spacing ---
    st.caption(
        "Tip: Click on any of the word buttons shown above to see example sentences for that word."
    )
    st.divider()

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

# TAB 6: Related word quiz
with tab6:
    st.title("📝 Related Word Quiz")

    # Load CSV data
    synonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_synonyms.csv")
    antonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_antonyms.csv")

    # Helper functions
    def get_related_words(df, word, prefix):
        row = df[df['word'] == word]
        if row.empty:
            return []
        return [row[f"{prefix}{i}"].values[0] for i in range(1, 4)
                if f"{prefix}{i}" in row and pd.notna(row[f"{prefix}{i}"].values[0]) and row[f"{prefix}{i}"].values[0] != '']

    # Build question list: each question is a dict with 'word', 'type' ('synonym'/'antonym'), 'correct', 'options'
    @st.cache_data
    def build_quiz_questions():
        questions = []
        all_words = sorted(set(synonyms_df['word']).union(set(antonyms_df['word'])))
        for word in all_words:
            syns = get_related_words(synonyms_df, word, 'synonym')
            ants = get_related_words(antonyms_df, word, 'antonym')
            # Synonym question
            if syns:
                correct = random.choice(syns)
                # Gather wrong options from antonyms or other synonyms
                wrongs = []
                for other_word in all_words:
                    if other_word != word:
                        wrongs += get_related_words(antonyms_df, other_word, 'antonym')
                        wrongs += get_related_words(synonyms_df, other_word, 'synonym')
                wrong_choices = random.sample([w for w in wrongs if w != correct], k=min(3, len([w for w in wrongs if w != correct])))
                options = wrong_choices + [correct]
                random.shuffle(options)
                questions.append({'word': word, 'type': 'synonym', 'correct': correct, 'options': options})
            # Antonym question
            if ants:
                correct = random.choice(ants)
                wrongs = []
                for other_word in all_words:
                    if other_word != word:
                        wrongs += get_related_words(synonyms_df, other_word, 'synonym')
                        wrongs += get_related_words(antonyms_df, other_word, 'antonym')
                wrong_choices = random.sample([w for w in wrongs if w != correct], k=min(3, len([w for w in wrongs if w != correct])))
                options = wrong_choices + [correct]
                random.shuffle(options)
                questions.append({'word': word, 'type': 'antonym', 'correct': correct, 'options': options})
        random.shuffle(questions)
        return questions

    # Session state initialization
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = build_quiz_questions()
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected = None

    questions = st.session_state.quiz_questions
    idx = st.session_state.quiz_index

    # Quiz in progress
    if idx < len(questions):
        q = questions[idx]
        st.markdown(f"### Which is a(n) {q['type']} of **{q['word']}**?")
        st.session_state.quiz_selected = st.radio(
            "Choose the correct answer:",
            q['options'],
            index=None if not st.session_state.quiz_answered else q['options'].index(q['correct'])
        )

        submit_col, next_col = st.columns([1, 2])
        with submit_col:
            if st.button("Submit Answer", disabled=st.session_state.quiz_answered):
                st.session_state.quiz_answered = True
                if st.session_state.quiz_selected == q['correct']:
                    st.session_state.quiz_score += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. The correct answer was: {q['correct']}")
        with next_col:
            if st.session_state.quiz_answered and st.button("Next Question ➡️"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_selected = None
                st.rerun()
        st.divider()
        st.markdown(f"**Progress:** {idx+1} / {len(questions)} &nbsp;&nbsp; **Score:** {st.session_state.quiz_score}")
    else:
        st.success("🎉 Quiz complete! You've gone through all the words.")
        st.markdown(f"**Final Score:** {st.session_state.quiz_score} / {len(questions)}")
        if st.button("Restart Quiz"):
            del st.session_state.quiz_questions
            del st.session_state.quiz_index
            del st.session_state.quiz_score
            del st.session_state.quiz_answered
            del st.session_state.quiz_selected
            st.rerun()
