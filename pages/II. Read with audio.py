import streamlit as st
from gtts import gTTS
import os
import tempfile

text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

sentences = text.split('. ')
sentences = [s.strip() + ('' if s.endswith('.') else '.') for s in sentences]

st.title("II. Read with audio")
tab1, tab2 = st.tabs(["Story", "Read with audio"])

with tab1:
    st.header("Story")
    st.write(text)

with tab2:
    st.header("sentence audio")

    tmp_dir = tempfile.mkdtemp()

    for i, sentence in enumerate(sentences):
        st.markdown(f"**{sentence}**")
        filename = os.path.join(tmp_dir, f"sentence_{i}.mp3")

        if not os.path.exists(filename):
            with st.spinner("Preparing audio..."):
                tts = gTTS(sentence)
                tts.save(filename)

        with open(filename, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
