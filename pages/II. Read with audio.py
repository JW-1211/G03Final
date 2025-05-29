import streamlit as st
from elevenlabs import generate, set_api_key
import io
import re

# ElevenLabs API 키 설정
set_api_key(sk_fa81c907489cb93db378208ac7a2ed1b905da3f2d2a6d0af)  # 여기에 본인의 API 키를 넣으세요

# 텍스트 원문
text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

# 문장 분리
sentences = re.split(r'(?<=[.!?])\s+', text.strip())

# Streamlit 앱 시작
st.title("3. 🔊 Read with audio")
tab1, tab2, tab3 = st.tabs(["1️⃣ 📖 Story", "2️⃣ 🅰️ Translation", "3️⃣ 🔊 Read with audio"])

# 📖 Story 탭
with tab1:
    st.header("📖 Story")
    highlighted_text = text
    highlight_words = ["Emma", "compass", "desire", "journey", "gallery", "art"]
    for word in highlight_words:
        highlighted_text = re.sub(rf"\b({word})\b", r'<mark style="background-color: #ffffcc">\1</mark>', highlighted_text)
    st.markdown(f"<div style='font-size: 20px; line-height: 1.6'>{highlighted_text}</div>", unsafe_allow_html=True)

# 🅰️ Translation 탭
with tab2:
    st.header("🅰️ Translation")
    translation = """
엠마는 어느 비 오는 오후 다락방에서 오래된 나침반을 발견했습니다. 그것은 단순한 나침반이 아니었고, 자기 북쪽이 아니라 가장 간절한 욕망을 가리켰습니다. 호기심에 이끌린 엠마는 나침반을 따라가며 이전과는 전혀 다른 방식으로 도시를 탐험하게 되었습니다.

나침반은 외로운 오래된 서점, 인적 없는 공원, 그리고 마지막으로 잊혀진 작은 미술관으로 그녀를 이끌었습니다. 각 장소에서 엠마는 자신도 몰랐던 문학, 자연, 예술에 대한 열정을 발견했습니다. 여정은 미술관에서 끝났고, 그곳에서 나침반은 멈췄습니다. 아름다운 그림들에 둘러싸여 엠마는 자신이 예술가가 되고 싶다는 것을 깨달았습니다.

영감을 받은 엠마는 집으로 돌아와 첫 그림을 그리기 시작했습니다. 이제 그 나침반은 그녀의 가장 소중한 소지품이 되어, 도시뿐 아니라 그녀의 꿈 속 길도 안내해주었습니다.
"""
    st.markdown(f"<div style='font-size: 19px; line-height: 1.7'>{translation}</div>", unsafe_allow_html=True)

# 🔊 Read with audio 탭
with tab3:
    st.header("🔊 Select a sentence to hear")

    numbered_sentences = [f"{i+1}. {s}" for i, s in enumerate(sentences)]
    selected = st.selectbox("Choose a sentence to play:", numbered_sentences)

    if st.button("Play Audio"):
        sentence_text = selected[selected.find(". ")+2:]  # 번호 제거
        st.markdown(f"<b>Selected sentence:</b> {sentence_text}", unsafe_allow_html=True)

        audio = generate(
            text=sentence_text,
            voice="Rachel",  # 원하는 voice 이름 (ElevenLabs 계정 내 음성에 따라 변경 가능)
            model="eleven_monolingual_v1"
        )
        st.audio(audio, format="audio/mp3")
