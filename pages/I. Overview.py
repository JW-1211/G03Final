import streamlit as st
from PIL import Image

st.title("I. Overview")

tab1, tab2, tab3 = st.tabs(["🧭 1. Guidelines", "🧩 2. Guess the story", "🗣️ 3. Share ideas"])

with tab1:
    st.subheader("Guidelines")
    st.write("""
    

 **✔ Before we start today’s lesson, let’s guess what the story is about!**

    
1.  Let’s try to guess the overall flow of the story based on the **four-panel comic picture**.

2.  Let’s try to predict the key words that appear in the story using the **word cloud**.

3. What do you think will happen to the main character? **Talk in your group!**

4. Make a sentence based on what your group guessed. **Try to make 1 or 2 sentences in English**.
""")


with tab2:
    st.subheader("Guess the story")
    st.write("Let's guess the story!")
    
    col1, col2 = st.columns(2)

    with col1:
        image1 = Image.open("images/CompassNumber.jpg")
        st.image(image1, caption="A four-panel comic picture", use_container_width=True)

    with col2:
        image2 = Image.open("images/Word cloud Enlgish.jpg)
        image3 = Image.open("image             
        st.image(image2, image3, caption="Word clouds", use_container_width=True)

from gtts import gTTS
import streamlit as st
import os
from io import BytesIO
import base64

with tab3:
    st.header("Let's share your ideas!")

    text_input = st.text_area("Type a sentence to hear it in English:", "")

    if st.button("Speak"):
        if text_input.strip() == "":
            st.warning("Please enter some text.")
        else:
            tts = gTTS(text_input, lang='en')
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            b64 = base64.b64encode(mp3_fp.read()).decode()
            audio_html = f"""
                <audio autoplay controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

