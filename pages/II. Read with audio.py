import streamlit as st
from gtts import gTTS
import io
import re

text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

sentences_raw = re.split(r'(?<=[.!?])\s+', text.strip())

translations = [
    "엠마는 비 오는 어느 날 오후 다락방에서 오래된 나침반을 발견했다.",
    "그건 평범한 나침반이 아니라 자기 북이 아니라 가장 큰 욕망을 가리키는 나침반이었다.",
    "엠마는 호기심에 이끌려 나침반이 가리키는 방향을 따라 도시를 여행하게 되었다.",
    "그 나침반은 그녀를 외로운 헌책방, 버려진 공원, 그리고 잊혀진 작은 미술관으로 이끌었다.",
    "각 장소에서 그녀는 자신의 숨겨진 열정인 문학, 자연, 예술을 발견했다.",
    "여정은 미술관에서 끝났고, 그곳에서 나침반은 멈췄다.",
    "아름다운 그림들 사이에서 엠마는 자신이 예술가가 되고 싶다는 열망을 깨달았다.",
    "영감을 받은 엠마는 집으로 돌아가 첫 그림을 그리기 시작했다.",
    "이제 나침반은 도시뿐만 아니라 그녀의 꿈을 이끄는 가장 소중한 물건이 되었다."
]

sentences = [f"{i+1}. {s}" for i, s in enumerate(sentences_raw)]

st.title("II. Read with audio")
tab1, tab2, tab3 = st.tabs(["Story", "Translation", "Read with audio"])

# Story Tab
with tab1:
    st.header("Story")
    st.markdown(
        f"""
        <div style="font-size:20px; line-height:1.6;">
        {text.replace('\n', '<br><br>')}
        </div>
        """,
        unsafe_allow_html=True
    )

# Translation Tab
with tab2:
    st.header("Translation")
    for i in range(len(sentences_raw)):
        st.markdown(f"**{i+1}. {sentences_raw[i]}**")
        st.markdown(f"→ {translations[i]}")

# Read with audio Tab
with tab3:
    st.header("Select a sentence to hear")

    selected_sentence = st.selectbox("Choose a sentence:", sentences)

    if st.button("Play Audio"):
        st.write(f"**Selected sentence:** {selected_sentence}")

        sentence_text = selected_sentence.split(". ", 1)[-1]

        tts = gTTS(text=sentence_text, lang='en')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        st.audio(audio_bytes, format='audio/mp3')

