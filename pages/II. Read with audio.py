import streamlit as st
from gtts import gTTS
import io
import re

st.title("📘 II. Read with Audio")
tab1, tab2, tab3 = st.tabs(["1. 📖 본문", "2. 🔤 해석", "3. 🔊 문장별 오디오"])

text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

translation = """
엠마는 어느 비 오는 오후 다락방에서 오래된 나침반을 발견했다. 그것은 단순한 나침반이 아니었고, 자석의 북쪽이 아니라 사람이 가장 간절히 원하는 것을 향해 가리켰다. 호기심에 이끌린 엠마는 그 나침반이 가리키는 방향을 따라 도시 곳곳을 여행하게 되었다.

나침반은 그녀를 외딴 헌책방, 한적한 공원, 그리고 결국 잊혀진 작은 미술관으로 이끌었다. 각 장소마다 엠마는 자신의 숨겨진 열정인 문학, 자연, 예술을 발견했다. 여행은 미술관에서 끝났고, 그곳에서 나침반은 멈췄다. 아름다운 그림들 속에서 엠마는 자신이 예술가가 되고 싶다는 열망을 깨달았다.

영감을 얻은 엠마는 집으로 돌아와 첫 그림을 그리기 시작했고, 나침반은 이제 단지 방향을 알려주는 물건이 아닌, 그녀의 꿈을 안내하는 소중한 존재가 되었다.
"""

# 강조할 단어 목록
highlight_words = ["Emma", "compass", "desire", "journey", "gallery", "art"]

# 단어 강조 처리
def highlight_text(text):
    for word in highlight_words:
        text = re.sub(rf'\b({word})\b', r'<mark style="background-color: #fdfd96a0">\1</mark>', text)
    return text

# 문장 분리
sentences = re.split(r'(?<=[.!?])\s+', text.strip())

# mp3 파일 미리 지정
elevenlabs_mp3 = {
    "Emma found an old compass in her attic one rainy afternoon.": "https://your-domain.com/audio/1.mp3",
    "Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.": "https://your-domain.com/audio/2.mp3"
}

# 탭 1 - 본문
with tab1:
    st.header("📖 영어 본문")
    st.markdown(f"<div style='font-size: 19px; line-height: 1.6'>{highlight_text(text)}</div>", unsafe_allow_html=True)

# 탭 2 - 해석
with tab2:
    st.header("🔤 해석")
    st.markdown(f"<div style='font-size: 18px; line-height: 1.6'>{translation.strip().replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

# 탭 3 - 문장별 오디오
with tab3:
    st.header("🔊 문장별 오디오 듣기")

    numbered_sentences = [f"{i+1}. {s}" for i, s in enumerate(sentences)]
    selected_display = st.selectbox("듣고 싶은 문장을 선택하세요:", numbered_sentences)
    selected_sentence = re.sub(r'^\d+\. ', '', selected_display)

    if st.button("Play Audio"):
        if selected_sentence in elevenlabs_mp3:
            st.audio(elevenlabs_mp3[selected_sentence], format='audio/mp3')
        else:
            tts = gTTS(text=selected_sentence, lang='en')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format='audio/mp3')

