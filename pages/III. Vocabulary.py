import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
from nltk.corpus import wordnet
import nltk

st.write("🌱 Vocabulary learning")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["❄️ 1. Lesson: Word list", "❄️ 2. Activity: Listen to the word", "❄️ 3. Spelling practice", "❄️ 4. Word relationships", "❄️ 5. Check your understanding"])

######### TAB 1


with tab1:
  st.markdown("### 📋 Word Frequency Table")

   # Load CSV from GitHub (update the link below)
  url = "https://raw.githubusercontent.com/JW-1211/streamlit25/refs/heads/main/word_frequency2.csv"
  df = pd.read_csv(url)

    # Show table only when button is clicked
  if st.button("Show Word List"):
     st.dataframe(df, use_container_width=True)


######### TAB 2 

with tab2:

  st.title("🔊 Word Pronunciation Practice")
  
  # --- Load CSV from GitHub ---

  url = "https://raw.githubusercontent.com/JW-1211/streamlit25/refs/heads/main/word_frequency2.csv"  # ← replace this!
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
    url = "https://raw.githubusercontent.com/JW-1211/streamlit25/refs/heads/main/word_frequency2.csv"  # Replace this!
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

with tab4:
    st.markdown("### 🔄 Synonyms and Anyonyms")
    st.caption("Enrich your vocabulary by learning how a single word can be expressed in different ways!")
    
    # Load CSV
    url = "https://raw.githubusercontent.com/JW-1211/streamlit25/refs/heads/main/word_frequency2.csv"
    try:
        df = pd.read_csv(url)
        
        if "Word" not in df.columns:
            st.error("CSV file must contain a 'Word' column")
        else:
            selected_word = st.selectbox("Choose a word to explore:", df["Word"].dropna().unique())
            
            if selected_word:
                try:
                    from thesaurus import Word
                    
                    # Initialize Thesaurus.com parser
                    word = Word(selected_word)
                    
                    # Get synonyms (all definitions, relevance 2-3)
                    synonyms = word.synonyms('all', relevance=[2,3], allowEmpty=False)
                    flat_synonyms = [item for sublist in synonyms for item in sublist]  # Flatten nested lists
                    
                    # Get antonyms (all definitions, relevance 2-3)
                    antonyms = word.antonyms('all', relevance=[2,3], allowEmpty=False)
                    flat_antonyms = [item for sublist in antonyms for item in sublist]
                    
                    # Remove duplicates and format
                    synonyms = list(set(flat_synonyms))
                    antonyms = list(set(flat_antonyms))
                    
                    # Display results
                    st.markdown("---")
                    
                    # Synonyms section
                    st.markdown("<h4 style='color:green;'>Synonyms</h4>", unsafe_allow_html=True)
                    if synonyms:
                        st.write(", ".join(synonyms))
                    else:
                        st.write("No synonyms found")
                    
                    # Antonyms section
                    st.markdown("<h4 style='color:red; margin-top:20px;'>Antonyms</h4>", unsafe_allow_html=True)
                    if antonyms:
                        st.write(", ".join(antonyms))
                    else:
                        st.write("No antonyms found")
                        
                except Exception as e:
                    st.error(f"Error processing word: {str(e)}")
                    st.info("Note: Thesaurus.com may have changed their website structure")
                    
    except Exception as e:
        st.error(f"Failed to load CSV: {str(e)}")

with tab5 : 
    st.write("### To be announced...")
