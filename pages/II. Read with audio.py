import streamlit as st
from elevenlabs import generate, play, set_api_key
import io
import re

set_api_key("sk_8d5dd83b03138c19dc86df513a5032734c4a5b3957fd3600")  

highlight_words = ["Emma", "compass", "desire", "journey", "gallery", "art"]
highlight_color = "#fff3b0"  # 형광펜 색상

text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

translation = """
엠마는 비 오는 어느 날 오후 다락방에서 오래된 나침반을 발견했습니다. 그것은 단순한 나침반이 아니라, 자석의 북쪽이 아닌 사람이 가장 바라는 것을 가리키는 나침반이었습니다. 엠마는 호기심에 이끌려 나침반을 따라 도시를 전혀 다른 시각으로 탐험하게 되었습니다.

나침반은 그녀를 외로운 헌책방, 인적이 드문 공원, 그리고 작은 잊힌 미술관으로 이끌었습니다. 각 장소에서 엠마는 문학, 자연, 예술과 같은 자신의 숨겨진 열정을 발견했습니다. 마지막 미술관에서 나침반은 멈췄고, 그녀는 화가가 되고 싶다는 자신의 열망을 깨달았습니다.

영감을 얻은 엠마는 집으로 돌아가 첫 그림을 그리기 시작했고, 나침반은 도시뿐만 아니라 그녀의 꿈도 이끄는 가장 소중한 물건이 되었습니다.
"""

sentences = re.split(r'(?<=[.!?])\s+', text.strip())

def highlight_text(text):
    for word in highlight_words:
        text = re.sub(f"\\b({word})\\b", f'<mark style="background-color: {highlight_color};">{word}</mark>', text)
    return text

st.set_page_config(page_title="Read with ElevenLabs Audio", layout="wide")
st.title("II. Read with audio")

tab1, tab2, tab3 = st.tabs([
    "1️⃣ 📖 Story",
    "2️⃣ 🅰️ Translation",
    "3️⃣ 🔊 Read with audio"
])

with tab1:
    st.header("📖 Original Story")
    st.markdown(f"<div style='font-size: 18px; line-height: 1.6;'>{highlight_text(text)}</div>", unsafe_allow_html=True)

with tab2:
    st.header("🅰️ 번역 보기")
    st.markdown(f"<div style='font-size: 18px; line-height: 1.6;'>{translation}</div>", unsafe_allow_html=True)

with tab3:
    st.header("🔊 문장별 오디오 듣기")

    numbered_sentences = [f"{i+1}. {s}" for i, s in enumerate(sentences)]
    selected = st.selectbox("문장을 선택하세요:", numbered_sentences)

    if st.button("▶️ Play with ElevenLabs"):
        selected_sentence = selected.split(". ", 1)[1]

        with st.spinner("Generating voice..."):
            audio = generate(
                text=selected_sentence,
                voice="Rachel",  
                model="eleven_monolingual_v1"
            )

            st.audio(audio, format="audio/mp3")
