import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random

st.write("Vocabulary learning")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💖 1. Lesson: Word list", "💖 2. Activity: Listen to the word", "💖 3. Spelling practice", "💖 4. Word relationships", "💖 5. Synonym/Antonym quiz"])

######### TAB 1


with tab1:
  st.markdown("### 📋 Word Table")

   # Load CSV from GitHub (update the link below)
  url = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"
  df = pd.read_csv(url)

    # Show table only when button is clicked
  if st.button("Show Word List"):
     st.dataframe(df, use_container_width=True)


######### TAB 2 

with tab2:

  st.title("🔊 Word Pronunciation Practice")
  
  # --- Load CSV from GitHub ---

  url = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"  # ← replace this!
  df = pd.read_csv(url)
  
  # --- Dropdown to select word ---
  st.markdown("## Select a word to hear its pronunciation")
  selected_word = st.selectbox("Choose a word:", df["Word"].dropna().unique())
  
  # --- Generate and play audio ---
  if selected_word:
      tts = gTTS(selected_word, lang='en')
      audio_fp = BytesIO()
      tts.write_to_fp(audio_fp)
      audio_fp.seek(0)
      st.audio(audio_fp, format='audio/mp3')


######### TAB 3

with tab3:
    st.markdown("### 🎧 Listen and Type the Word")
    st.caption("Click the button to hear a word. Then type it and press 'Check the answer'.")

    # Load CSV
    url = "https://raw.githubusercontent.com/JW-1211/G03Final/main/data/vocabulary.csv"  # Replace this!
    df = pd.read_csv(url)
    word_list = df["Word"].dropna().tolist()

    # Initialize session state variables
    if "current_word" not in st.session_state:
        st.session_state.current_word = None
    if "audio_data" not in st.session_state:
        st.session_state.audio_data = None
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "check_clicked" not in st.session_state:
        st.session_state.check_clicked = False

    # ▶️ Button to select and play a new random word
    if st.button("🔊 Let me listen to a word"):
        st.session_state.current_word = random.choice(word_list)
        st.session_state.user_input = ""
        st.session_state.check_clicked = False

        tts = gTTS(st.session_state.current_word, lang='en')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.session_state.audio_data = audio_fp.read()

    # 🎧 Audio playback
    if st.session_state.audio_data:
        st.audio(st.session_state.audio_data, format='audio/mp3')

    # ✏️ Text input
    st.session_state.user_input = st.text_input("Type the word you heard:", value=st.session_state.user_input)

    # ✅ Check answer button
    if st.button("✅ Check the answer"):
        st.session_state.check_clicked = True

    # 💬 Give feedback only after clicking the check button
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
