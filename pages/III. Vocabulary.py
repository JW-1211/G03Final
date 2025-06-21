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
    import pandas as pd, random, streamlit as st          # ← keep imports local to this tab

    # 1️⃣  DATA (unchanged)
    synonyms_df = pd.read_csv(
        "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_synonyms.csv"
    )
    antonyms_df = pd.read_csv(
        "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_antonyms.csv"
    )

    # 2️⃣  HELPERS  – defined INSIDE the tab so they don’t run elsewhere  [1]
    def get_related(df, word, kind):
        row = df[df["word"] == word]
        if row.empty:
            return []
        return [
            row[f"{kind}{i}"].values[0]
            for i in range(1, 4)
            if f"{kind}{i}" in row
            and pd.notna(row[f"{kind}{i}"].values[0])
            and row[f"{kind}{i}"].values[0] != ""
        ]

    def new_question():
        all_words = set(synonyms_df.word) | set(antonyms_df.word)

        syn_pool = [
            w
            for w in all_words
            if w not in st.session_state.tab6_used_syn
            and get_related(synonyms_df, w, "synonym")
        ]
        ant_pool = [
            w
            for w in all_words
            if w not in st.session_state.tab6_used_ant
            and get_related(antonyms_df, w, "antonym")
        ]

        if not syn_pool and not ant_pool:        # quiz finished
            return None

        qtype = random.choice(
            (["synonym"] if syn_pool else []) + (["antonym"] if ant_pool else [])
        )

        if qtype == "synonym":
            target = random.choice(syn_pool)
            st.session_state.tab6_used_syn.add(target)
            correct = get_related(synonyms_df, target, "synonym")
            wrong_pool = get_related(antonyms_df, target, "antonym")
        else:
            target = random.choice(ant_pool)
            st.session_state.tab6_used_ant.add(target)
            correct = get_related(antonyms_df, target, "antonym")
            wrong_pool = get_related(synonyms_df, target, "synonym")

        if len(wrong_pool) < 3:
            extra = [
                w
                for w in all_words
                if w != target and w not in correct and w not in wrong_pool
            ]
            wrong_pool += random.sample(extra, min(3 - len(wrong_pool), len(extra)))

        options = random.sample(wrong_pool, min(3, len(wrong_pool))) + [
            random.choice(correct)
        ]
        random.shuffle(options)
        return {"word": target, "type": qtype, "correct": correct, "options": options}

    # 3️⃣  SESSION STATE (unique keys prefixed with tab6_)                [1]
    for k, v in {
        "tab6_score": 0,
        "tab6_total": 0,
        "tab6_used_syn": set(),
        "tab6_used_ant": set(),
        "tab6_question": None,
        "tab6_answered": False,
    }.items():
        st.session_state.setdefault(k, v)

    if st.session_state.tab6_question is None:
        st.session_state.tab6_question = new_question()

    # 4️⃣  UI
    st.title("📝 Related-word Quiz (Tab 6)")

    q = st.session_state.tab6_question
    if q is None:
        st.success(
            f"🎉 Finished! Final score: {st.session_state.tab6_score} / "
            f"{st.session_state.tab6_total}"
        )
        if st.button("Retake Quiz", key="tab6_retake"):
            for key in (
                "tab6_score",
                "tab6_total",
                "tab6_used_syn",
                "tab6_used_ant",
                "tab6_question",
                "tab6_answered",
            ):
                del st.session_state[key]
            st.experimental_rerun()
    else:
        st.markdown(f"### Pick a **{q['type']}** of *{q['word']}*")
        choice = st.radio(
            "Options",
            q["options"],
            key="tab6_radio",
            disabled=st.session_state.tab6_answered,
        )

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button(
                "Submit",
                key="tab6_submit",
                disabled=st.session_state.tab6_answered,
            ):
                st.session_state.tab6_answered = True
                st.session_state.tab6_total += 1
                if choice == q["correct"]:
                    st.session_state.tab6_score += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ The right answer was **{q['correct']}**")

        with col2:
            if st.session_state.tab6_answered and st.button(
                "Next Question ➡️", key="tab6_next"
            ):
                st.session_state.tab6_question = new_question()
                st.session_state.tab6_answered = False
                st.experimental_rerun()

        st.markdown(
            f"**Score:** {st.session_state.tab6_score} / {st.session_state.tab6_total}"
        )
