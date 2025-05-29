import streamlit as st
import re
import os
import sys
import subprocess

# 💡 자동 패키지 설치
required = ['elevenlabs']
for pkg in required:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

from elevenlabs import generate, set_api_key
import base64

# 🗝️ API 키 설정 (보안상 실제 키는 환경변수로 처리 권장)
set_api_key("sk_fa81c907489cb93db378208ac7a2ed1b905da3f2d2a6d0af")  # 여기에 실제 API 키 입력

# 📖 텍스트와 문장 분리
text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

translation = """
엠마는 어느 비 오는 오후, 다락방에서 오래된 나침반을 발견했습니다. 이건 평범한 나침반이 아니었어요—자신의 가장 큰 욕망을 가리키는 나침반이었죠. 호기심에 사로잡힌 엠마는 나침반을 따라 도시를 새롭게 탐험하기 시작했습니다.

그 여정은 오래된 서점, 버려진 공원, 그리고 잊혀진 작은 미술관으로 이어졌습니다. 각 장소마다 그녀는 문학, 자연, 예술과 같은 자신의 숨겨진 열정을 발견했습니다. 여정은 미술관에서 멈췄고, 나침반도 그곳에서 멈췄습니다. 아름다운 그림들 사이에서 엠마는 자신이 예술가가 되고 싶다는 걸 깨달았어요.

영감을 얻은 엠마는 집으로 돌아가 첫 그림을 그리기 시작했습니다. 이제 나침반은 도시뿐 아니라 그녀의 꿈을 향한 길잡이가 되었죠.
"""

# 🎯 문장 나누기 및 강조 단어 설정
sentences = re.split(r'(?<=[.!?])\s+', text.strip())
highlight_words = ["Emma", "compass", "desire", "journey", "gallery", "art"]

# 📚 탭 구성
tab1, tab2, tab3 = st.tabs(["1️⃣ 📖 본문", "2️⃣ 🅰️ 해석", "3️⃣ 🔊 문장별 오디오"])

# ✨ 하이라이트 함수
def highlight_text(text, words):
    for word in words:
        text = re.sub(rf'\b({re.escape(word)})\b', r'<mark style="background-color: #ffff88a0">\1</mark>', text)
    return text

# 📖 탭 1 - 원문
with tab1:
    st.markdown("### 📖 Story")
    st.markdown(f"<div style='font-size:18px; line-height:1.6'>{highlight_text(text, highlight_words)}</div>", unsafe_allow_html=True)

# 🅰️ 탭 2 - 해석
with tab2:
    st.markdown("### 🅰️ 번역")
    st.markdown(f"<div style='font-size:18px; line-height:1.6'>{translation}</div>", unsafe_allow_html=True)

# 🔊 탭 3 - 오디오
with tab3:
    st.markdown("### 🔊 문장별 오디오 듣기")
    for i, sentence in enumerate(sentences, 1):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"**{i}.** {sentence}")
        with col2:
            if st.button(f"▶️", key=f"btn_{i}"):
                audio = generate(text=sentence, voice="Rachel", model="eleven_monolingual_v1")
                b64 = base64.b64encode(audio).decode()
                st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
