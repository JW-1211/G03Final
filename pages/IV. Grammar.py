import streamlit as st
from gtts import gTTS
from io import BytesIO
import random
import pandas as pd

st.title("🌱 Grammar Learning")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Past Tense Video",
    "2. Understanding Past Tense",
    "3. Pronunciation Practice",
    "4. Regular Verb Quiz",
    "5. Irregular Verb Quiz"
])

######### TAB 1 - Past Tense Video

with tab1:
    st.title("Understanding Past Tense")
    st.video("https://youtu.be/q6j-D5EzZo8", start_time=0)

######### TAB 2 - Understanding Past Tense

with tab2:
    st.markdown("## 📋 Understanding Past Tense")
    st.write("Let's Learn About the Past Tense!")

    # Introduction
    st.header("What is the Past Tense?")
    st.write("The past tense is used to talk about actions that have already happened.")

    # Regular Verbs Section
    st.header("Regular Verbs")
    st.write("Forming Regular Past Tense:")
    st.write("1. General Rule: Add -ed (e.g., walk → walked)")
    st.write("2. Ending with 'e': Add -d (e.g., love → loved)")
    st.write("3. Single Vowel + Consonant: Double the consonant, add -ed (e.g., stop → stopped)")
    st.write("4. Ending with 'y': Change 'y' to 'i', add -ed (e.g., cry → cried)")

    # Irregular Verbs Section
    st.header("Irregular Verbs")
    st.write("Irregular verbs do not follow standard rules. Here are some examples:")

    irregular_verbs_data = {
        "Base Form": ["Find", "Become", "Be", "Begin", "Break", "Bring", "Buy", "Choose", "Come", "Do", "Drink", "Drive", "Eat", "Fall", "Feel", "Get", "Go", "Have", "Know", "Leave", "Make", "Read", "Run", "Say", "See", "Send", "Sing", "Speak", "Take", "Write"],
        "Past Tense": ["Found", "Became", "Was/Were", "Began", "Broke", "Brought", "Bought", "Chose", "Came", "Did", "Drank", "Drove", "Ate", "Fell", "Felt", "Got", "Went", "Had", "Knew", "Left", "Made", "Read", "Ran", "Said", "Saw", "Sent", "Sang", "Spoke", "Took", "Wrote"],
        "Past Participle": ["Found", "Become", "Been", "Begun", "Broken", "Brought", "Bought", "Chosen", "Come", "Done", "Drunk", "Driven", "Eaten", "Fallen", "Felt", "Gotten", "Gone", "Had", "Known", "Left", "Made", "Read", "Run", "Said", "Seen", "Sent", "Sung", "Spoken", "Taken", "Written"]
    }

    irregular_verbs_df = pd.DataFrame(irregular_verbs_data)
    st.table(irregular_verbs_df)

    # Add the new section for stories with past tense forms
    st.header("Stories with Past Tense Forms")
    st.write("Here is a table of verbs used in stories with their past and past participle forms:")

    # Combine regular and irregular verbs into one table
    combined_verb_data = {
        "Base Form": ["Discover", "End", "Realize", "Inspire", "Start", "Find", "Become", "Be"],
        "Simple Past": ["Discovered", "Ended", "Realized", "Inspired", "Started", "Found", "Became", "Was/Were"],
        "Past Participle": ["Discovered", "Ended", "Realized", "Inspired", "Started", "Found", "Become", "Been"]
    }

    combined_verbs_df = pd.DataFrame(combined_verb_data)
    st.table(combined_verbs_df)

######### TAB 3 - Pronunciation Practice

with tab3:
    st.title("🔊 Pronunciation Practice")

    # Define the lists of verbs
    regular_verbs = {
        "discover": "discovered",
        "end": "ended",
        "realize": "realized",
        "inspire": "inspired",
        "start": "started"
    }
    irregular_verbs = {
        "be": ("was/were", "been"),
        "become": ("became", "become"),
        "begin": ("began", "begun"),
        "break": ("broke", "broken"),
        "bring": ("brought", "brought"),
        "build": ("built", "built"),
        "buy": ("bought", "bought"),
        "catch": ("caught", "caught"),
        "choose": ("chose", "chosen"),
        "come": ("came", "come"),
        "do": ("did", "done"),
        "drink": ("drank", "drunk"),
        "drive": ("drove", "driven"),
        "eat": ("ate", "eaten"),
        "fall": ("fell", "fallen"),
        "feel": ("felt", "felt"),
        "get": ("got", "gotten"),
        "go": ("went", "gone"),
        "have": ("had", "had"),
        "know": ("knew", "known"),
        "leave": ("left", "left"),
        "make": ("made", "made"),
        "read": ("read", "read"),
        "run": ("ran", "run"),
        "say": ("said", "said"),
        "see": ("saw", "seen"),
        "send": ("sent", "sent"),
        "sing": ("sang", "sung"),
        "speak": ("spoke", "spoken"),
        "take": ("took", "taken"),
        "write": ("wrote", "written")
    }

    # Regular Verbs Section
    st.header("Regular Verbs Pronunciation")
    selected_regular_verb = st.selectbox("Select a regular verb:", list(regular_verbs.keys()), key="regular")

    if selected_regular_verb:
        past_form = regular_verbs[selected_regular_verb]
        past_participle = past_form  # 규칙동사는 과거형=과거분사
        st.write(f"Base form: {selected_regular_verb}, Past tense: {past_form}, Past participle: {past_participle}")

        try:
            forms = [selected_regular_verb, past_form, past_participle]
            combined_audio_fp = BytesIO()
            for form in forms:
                tts = gTTS(form)
                tts.write_to_fp(combined_audio_fp)
            combined_audio_fp.seek(0)
            st.audio(combined_audio_fp, format="audio/mp3")
        except Exception as e:
            st.error(f"Error generating audio: {e}")

    # Irregular Verbs Section
    st.header("Irregular Verbs Pronunciation")
    selected_irregular_verb = st.selectbox("Select an irregular verb:", list(irregular_verbs.keys()), key="irregular")

    if selected_irregular_verb:
        past_tense, past_participle = irregular_verbs[selected_irregular_verb]
        st.write(f"Base form: {selected_irregular_verb}, Past tense: {past_tense}, Past participle: {past_participle}")

        try:
            forms = [selected_irregular_verb, past_tense, past_participle]
            combined_audio_fp = BytesIO()
            for form in forms:
                tts = gTTS(form)
                tts.write_to_fp(combined_audio_fp)
            combined_audio_fp.seek(0)
            st.audio(combined_audio_fp, format="audio/mp3")
        except Exception as e:
            st.error(f"Error generating audio: {e}")

######### TAB 4 - Regular Verb Quiz

with tab4:
    st.title("Regular Verb Quiz")

    # List of regular verbs and their past tense forms with rules
    regular_verbs_explained = {
        "discover": ("discovered", "General Rule: Add -ed (e.g., walk → walked)"),
        "end": ("ended", "General Rule: Add -ed (e.g., walk → walked)"),
        "realize": ("realized", "Ending with e: Add -d (e.g., love → loved)"),
        "inspire": ("inspired", "Ending with e: Add -d (e.g., love → loved)"),
        "start": ("started", "Single Vowel + Consonant: Double the consonant, add -ed (e.g., stop → stopped)")
    }

    # Initialize session state variables
    if "current_regular_verb" not in st.session_state:
        st.session_state.current_regular_verb = None
    if "regular_user_input" not in st.session_state:
        st.session_state.regular_user_input = ""
    if "regular_check_clicked" not in st.session_state:
        st.session_state.regular_check_clicked = False

    # Button to select a new random regular verb
    if st.button("🎲 Get a new regular verb", key="regular_button"):
        st.session_state.current_regular_verb = random.choice(list(regular_verbs_explained.keys()))
        st.session_state.regular_user_input = ""
        st.session_state.regular_check_clicked = False

    # Display the current regular verb
    if st.session_state.current_regular_verb:
        base_form = st.session_state.current_regular_verb
        past_form, explanation = regular_verbs_explained[base_form]

        st.write(f"Base form: **{base_form}**")

        # Text input for user's answer
        st.session_state.regular_user_input = st.text_input("Enter the past tense form:", value=st.session_state.regular_user_input, key="regular_input")

        # Button to check the answer
        if st.button("✅ Check the answer", key="regular_check_button"):
            st.session_state.regular_check_clicked = True

        # Feedback
        if st.session_state.regular_check_clicked:
            if st.session_state.regular_user_input.strip().lower() == past_form:
                st.success(f"✅ Correct! {explanation}")
            else:
                st.error(f"❌ Incorrect. The correct past tense is: **{past_form}**")

######### TAB 5 - Irregular Verb Quiz

with tab5:
    st.title("Irregular Verb Quiz")

    # Initialize session state variables
    if "current_verb" not in st.session_state:
        st.session_state.current_verb = None
    if "user_input_past" not in st.session_state:
        st.session_state.user_input_past = ""
    if "user_input_participle" not in st.session_state:
        st.session_state.user_input_participle = ""
    if "check_clicked" not in st.session_state:
        st.session_state.check_clicked = False

    # Button to select a new random verb
    if st.button("🎲 Get a new verb", key="irregular_button"):
        st.session_state.current_verb = random.choice(list(irregular_verbs.keys()))
        st.session_state.user_input_past = ""
        st.session_state.user_input_participle = ""
        st.session_state.check_clicked = False

    # Display the current verb
    if st.session_state.current_verb:
        st.write(f"Base form: **{st.session_state.current_verb}**")

        # Text input for user's answers
        st.session_state.user_input_past = st.text_input("Enter the past tense form:", value=st.session_state.user_input_past, key="past_input")
        st.session_state.user_input_participle = st.text_input("Enter the past participle form:", value=st.session_state.user_input_participle, key="participle_input")

        # Button to check the answer
        if st.button("✅ Check the answers", key="irregular_check_button"):
            st.session_state.check_clicked = True

        # Feedback
        if st.session_state.check_clicked:
            correct_past, correct_participle = irregular_verbs[st.session_state.current_verb]
            past_correct = st.session_state.user_input_past.strip().lower() == correct_past
            participle_correct = st.session_state.user_input_participle.strip().lower() == correct_participle

            if past_correct and participle_correct:
                st.success("✅ Both answers are correct!")
            else:
                st.error("❌ Incorrect. You need to get both forms right.")
                if not past_correct:
                    st.info(f"The correct past tense is: **{correct_past}**")
                if not participle_correct:
                    st.info(f"The correct past participle is: **{correct_participle}**")
