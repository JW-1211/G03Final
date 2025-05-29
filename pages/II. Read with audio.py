import streamlit as st
from elevenlabs import generate, set_api_key
import os

# ElevenLabs API 키 설정
set_api_key("sk_fa81c907489cb93db378208ac7a2ed1b905da3f2d2a6d0af")

# 중요한 단어 강조용 함수
def highlight_keywords(text, keywords):
    for word in keywords:
        text = text.replace(word, f"<mark style='background-color: rgba(255, 255, 0, 0.4)'>{word}</mark>")
    return text

# 텍스트 및 문장
text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

sentences = [
    "Emma found an old compass in her attic one rainy afternoon.",
    "It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north.",
    "Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.",
    "The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery.",
    "At each stop, she discovered pieces of her own hidden passions: literature, nature, and art.",
    "The journey ended at the gallery, where the compass stopped moving.",
    "There, surrounded by beautiful paintings, Emma realized her desire to become an artist.",
    "Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams."
]

# 중요한 단어 목록
keywords = ["Emma", "compass", "desire", "journey", "gallery", "art"]

# mp3 저장 디렉토리
audio_dir = "audio"
os.makedirs(audio_dir, exist_ok=True)

# 오디오 파일 생성
for idx, sentence in enumerate(sentences):
    file_path = os.path.join(audio_dir, f"sentence_{idx+1}.mp3")
    if not os.path.exists(file_path):
        audio = generate(text=sentence, voice="Rachel", model="eleven_monolingual_v1")
        with open(file_path, "wb") as f:
            f.write(audio)

# Streamlit 앱 UI
st.set_page_config(page_title="Read with Audio", layout="centered")
st.title("🎧 II. Read with Audio")

tab1, tab2, tab3 = st.tabs(["1️⃣ 📖 본문", "2️⃣ 🅰️ 해석", "3️⃣ 🔊 문장별 오디오"])

with tab1:
    st.header("📖 Story")
    highlighted = highlight_keywords(text.strip(), keywords)
    st.markdown(f"<div style='font-size: 20px; line-height: 1.6'>{highlighted}</div>", unsafe_allow_html=True)

with tab2:
    st.header("🅰️ 해석")
    # 여기에 한국어 번역 넣기 (간단 번역 예시)
    translation = """
    엠마는 비 오는 오후 다락방에서 오래된 나침반을 발견했다. 그것은 평범한 나침반이 아니라, 자석 북쪽이 아니라 사람의 가장 큰 욕망을 가리켰다.
    엠마는 호기심에 이끌려 나침반이 가리키는 방향을 따라 도시 곳곳을 여행했다.

    나침반은 외로운 헌책방, 버려진 공원, 그리고 작은 미술관으로 그녀를 이끌었다. 각 장소에서 엠마는 자신이 숨겨온 열정을 발견했다.
    마지막 장소인 미술관에서 나침반은 멈췄고, 그녀는 예술가가 되고 싶은 열망을 깨달았다.

    엠마는 집으로 돌아가 첫 그림을 그리기 시작했고, 나침반은 이제 그녀의 꿈을 안내하는 가장 소중한 보물이 되었다.
    """
    st.markdown(f"<div style='font-size: 19px; line-height: 1.8'>{translation.strip()}</div>", unsafe_allow_html=True)

with tab3:
    st.header("🔊 문장별 오디오 듣기")
    selected = st.selectbox("문장을 선택하세요:", [f"{i+1}. {s}" for i, s in enumerate(sentences)])

    if st.button("▶️ 재생"):
        index = int(selected.split(".")[0]) - 1
        st.audio(os.path.join(audio_dir, f"sentence_{index+1}.mp3"), format="audio/mp3")

