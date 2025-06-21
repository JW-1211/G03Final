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
    st.title("📝 Related Word Quiz")

# Load CSV data
synonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_synonyms.csv")
antonyms_df = pd.read_csv("https://raw.githubusercontent.com/JW-1211/G03Final/main/data/test_antonyms.csv")

def get_related_words(df, word, prefix):
    row = df[df['word'] == word]
    if row.empty:
        return []
    return [row[f"{prefix}{i}"].values[0] for i in range(1, 4)
            if f"{prefix}{i}" in row and pd.notna(row[f"{prefix}{i}"].values[0]) and row[f"{prefix}{i}"].values[0] != '']

def generate_quiz_question():
    # --- START OF MINIMAL CHANGES in this function ---
    
    # Get all possible words and filter out the ones already used
    all_words_pool = set(synonyms_df['word']).union(set(antonyms_df['word']))
    unused_words = [word for word in all_words_pool if word not in st.session_state.used_words]

    # If no unused words are left, the quiz is over
    if not unused_words:
        return None
    
    question_type = random.choice(['synonym', 'antonym'])
    valid_words = []
    
    # Iterate over ONLY the unused words to find a valid question
    for word in unused_words:
        if question_type == 'synonym' and len(get_related_words(synonyms_df, word, 'synonym')) > 0:
            valid_words.append(word)
        elif question_type == 'antonym' and len(get_related_words(antonyms_df, word, 'antonym')) > 0:
            valid_words.append(word)
            
    if not valid_words:
        return None # Return None if no valid question can be formed from remaining words
        
    target_word = random.choice(valid_words)
    
    # Add the chosen word to the set of used words
    st.session_state.used_words.add(target_word)

    # --- END OF MINIMAL CHANGES in this function ---
    
    if question_type == 'synonym':
        correct_answers = get_related_words(synonyms_df, target_word, 'synonym')
        wrong_pool = get_related_words(antonyms_df, target_word, 'antonym')
    else:
        correct_answers = get_related_words(antonyms_df, target_word, 'antonym')
        wrong_pool = get_related_words(synonyms_df, target_word, 'synonym')
        
    all_words = set(synonyms_df['word']).union(set(antonyms_df['word']))
    if len(wrong_pool) < 3:
        additional_wrong = [w for w in all_words if w != target_word and w not in correct_answers]
        wrong_pool += random.sample(additional_wrong, min(3-len(wrong_pool), len(additional_wrong)))
        
    wrong_answers = random.sample(wrong_pool, 3) if len(wrong_pool) >=3 else wrong_pool
    correct_answer = random.choice(correct_answers)
    options = wrong_answers + [correct_answer]
    random.shuffle(options)
    
    return {
        'word': target_word,
        'correct': correct_answer,
        'options': options,
        'type': question_type
    }

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
    
# --- NEW --- Initialize the set for used words
if 'used_words' not in st.session_state:
    st.session_state.used_words = set()
    
if 'current_question' not in st.session_state:
    st.session_state.current_question = generate_quiz_question()
if 'answered' not in st.session_state:
    st.session_state.answered = False

q = st.session_state.current_question

# --- MODIFIED --- Added an 'else' block to handle quiz completion
if q:
    st.markdown(f"### Which is a(an) {q['type']} of **{q['word']}**?")
    selected = st.radio("Choose the correct answer:", q['options'])
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Submit Answer", disabled=st.session_state.answered):
            st.session_state.answered = True
            st.session_state.total += 1
            if selected == q['correct']:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer was: {q['correct']}")
    with col2:
        if st.session_state.answered:
            if st.button("Next Question ➡️"):
                st.session_state.current_question = generate_quiz_question()
                st.session_state.answered = False
                st.rerun()
                
    st.divider()
    st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.total}")
else:
    # This message appears when all words have been used
    st.success("🎉 Quiz complete! You have gone through all the available words.")
    st.markdown(f"### **Final Score:** {st.session_state.score} / {st.session_state.total}")
