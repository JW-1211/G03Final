import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import random
import requests

API_NINJAS_KEY = "e+bJafR3fh0DLmxfRkUZfg==GEtwBoUf9Y8wAkyI"

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
                api_url = f"https://api.api-ninjas.com/v1/thesaurus?word={selected_word}"
                headers = {'X-Api-Key': API_NINJAS_KEY}
                try:
                    response = requests.get(api_url, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    synonyms = data.get('synonyms', [])
                    antonyms = data.get('antonyms', [])

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

                except Exception as e:
                    st.error(f"API error: {e}")
    except Exception as e:
        st.error(f"Failed to load CSV: {e}")

with tab5 : 

# Configuration
CSV_URL = "https://raw.githubusercontent.com/JW-1211/streamlit25/main/word_frequency2.csv"
API_URL = "https://api.api-ninjas.com/v1/thesaurus"
API_KEY = "e+bJafR3fh0DLmxfRkUZfg==GEtwBoUf9Y8wAkyI"  # Replace with your API Ninjas key

@st.cache_data
def load_word_list():
    df = pd.read_csv(CSV_URL)
    if 'Frequency' in df.columns:
        df = df.sort_values('Frequency', ascending=False)
    return df['Word'].dropna().tolist()

def get_word_relations(word):
    try:
        response = requests.get(f"{API_URL}?word={word}", headers={'X-Api-Key': API_KEY})
        response.raise_for_status()
        data = response.json()
        return {
            'synonyms': data.get('synonyms', [])[:10],
            'antonyms': data.get('antonyms', [])[:10]
        }
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def generate_quiz_pair():
    words = load_word_list()
    
    for word in words:
        relations = get_word_relations(word)
        if relations and len(relations['synonyms']) >= 1 and len(relations['antonyms']) >= 3:
            # Synonym Quiz Options (1 synonym + 3 antonyms)
            synonym_answer = random.choice(relations['synonyms'])
            synonym_distractors = random.sample(relations['antonyms'], 3)
            synonym_options = [synonym_answer] + synonym_distractors
            random.shuffle(synonym_options)
            
            # Antonym Quiz Options (1 antonym + 3 synonyms)
            antonym_answer = random.choice(relations['antonyms'])
            antonym_distractors = random.sample(relations['synonyms'], 3)
            antonym_options = [antonym_answer] + antonym_distractors
            random.shuffle(antonym_options)
            
            return {
                'word': word,
                'synonym_quiz': {
                    'question': f"Which of the following is a synonym of '{word}'?",
                    'options': synonym_options,
                    'correct': synonym_answer
                },
                'antonym_quiz': {
                    'question': f"Which of the following is an antonym of '{word}'?",
                    'options': antonym_options,
                    'correct': antonym_answer
                }
            }
    
    st.error("Could not generate quiz questions. Some words may lack sufficient relations.")
    return None

def quiz_section(quiz_data, quiz_type):
    st.markdown(f"### {quiz_data['question']}")
    selected = st.radio("Options:", quiz_data['options'], key=f"options_{quiz_type}")
    
    if st.button("Check Answer", key=f"check_{quiz_type}"):
        if selected == quiz_data['correct']:
            st.success("✅ Correct! Well done!")
            st.session_state[f'score_{quiz_type}'] += 1
        else:
            st.error(f"❌ Incorrect. The correct answer was: {quiz_data['correct']}")
        
        st.markdown(f"**Current Score:** {st.session_state[f'score_{quiz_type}']}")
        
        if st.button("Next Word", key=f"next_{quiz_type}"):
            st.session_state.current_pair = generate_quiz_pair()
            st.experimental_rerun()

def main():
    st.title("Vocabulary Dual Challenge 🔄")
    
    if 'current_pair' not in st.session_state:
        st.session_state.current_pair = generate_quiz_pair()
        st.session_state.score_synonym = 0
        st.session_state.score_antonym = 0

    if st.session_state.current_pair:
        current_word = st.session_state.current_pair['word']
        st.markdown(f"## Current Word: **{current_word}**")
        
        # Synonym Quiz
        st.markdown("---")
        quiz_section(st.session_state.current_pair['synonym_quiz'], 'synonym')
        
        # Antonym Quiz
        st.markdown("---")
        quiz_section(st.session_state.current_pair['antonym_quiz'], 'antonym')

if __name__ == "__main__":
    main()
