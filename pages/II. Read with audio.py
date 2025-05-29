import streamlit as st
from elevenlabs import generate, set_api_key
import io
import re

set_api_key(st.secrets["elevenlabs_api_key"])

highlight_words = ["Emma", "compass", "desire", "journey", "gallery", "art"]

text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

translation = """
엠마는 어느 비 오는 오후 다락방에서 오래된 나침반을 발견했다. 그것은 평범한 나침반이 아니라 자석이 아닌, 사람의 가장 큰 욕망을 가리켰다. 엠마는 호기심에 이끌려 나침반을 따라 도시를 새롭게 탐험하기 시작했다.

그 여정은 외로운 헌책방, 버려진 공원, 그리고 잊힌 작은 미술관으로 이어졌다. 그녀는 각각의 장소에서 자신이 사랑했던 문학, 자연, 예술을 다시 발견했다. 마지막 장소인 미술관에 도착했을 때 나침반은 멈췄고, 엠마는 자신이 예술가가 되고 싶다는 열망을 깨달았다.

엠마는 영감을 받아 첫 그림을 그리기 시작했고, 나침반은 이제 도시뿐 아니라 그녀의 꿈을 안내하는 가장 소중한 물건이 되었다.
"""

sentences = re.split(r'(?<=[.!?])\s+', text.strip())

def highlight_keywords(sentence):
    for word in highlight_words:
        sentence = re.sub(fr'\b({word})\b', r'<mark style="background-color: #ffff66aa">\1</mark>', sentence)
    return sentence

st.set_page_config(page_title="Read with Audio", layout="centered")
st.title("II. Read with audio")

tab1, tab2, tab3 = st.tabs(["1️⃣ 📘 본문", "2️⃣ 🔤 해석", "3️⃣ 🔊 문장별 오디오"])

with tab1:
    st.header("📘 이야기 본문")
    styled_text = "<br><br>".join([highlight_keywords(p) for p in text.strip().split('\n') if p])
    st.markdown(f"<div style='font-size: 18px; line-height: 1.6'>{styled_text}</div>", unsafe_allow_html=True)

with tab2:
    st.header("🔤 이야기 해석")
    translated_text = "<br><br>".join([p.strip() for p in translation.strip().split('\n') if p])
    st.markdown(f"<div style='font-size: 17px; line-height: 1.8'>{translated_text}</div>", unsafe_allow_html=True)

with tab3:
    st.header("🔊 문장별 오디오 듣기")
    for i, sentence in enumerate(sentences):
        col1, col2 = st.columns([8, 2])
        with col1:
            st.markdown(f"**{i+1}.** {sentence}")
        with col2:
            if st.button(f"▶️ 재생 {i+1}", key=f"btn_{i}"):
                audio = generate(text=sentence, voice="Rachel", model="eleven_multilingual_v2")
                st.audio(audio, format="audio/mp3")
