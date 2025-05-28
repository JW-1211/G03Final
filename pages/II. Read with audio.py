import streamlit as st
from gtts import gTTS
import io
import re

# 원문 텍스트
text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

# 문장 나누기 (빈 문장 제거 포함)
sentences_raw = [s for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]

# 해석 (예시로 간단한 번역 추가)
translations = [
    "엠마는 비 오는 오후 다락방에서 오래된 나침반을 발견했습니다.",
    "그것은 평범한 나침반이 아니었고, 자기 북쪽이 아닌 사람의 가장 큰 욕망을 가리켰습니다.",
    "엠마는 호기심에 이끌려 나침반이 가리키는 방향을 따라갔고, 전에 없던 방식으로 도시를 여행하게 되었습니다.",
    "나침반은 그녀를 외로운 오래된 서점, 버려진 공원, 그리고 결국 작고 잊힌 미술관으로 이끌었습니다.",
    "각 장소에서 그녀는 자신의 숨겨진 열정인 문학, 자연, 예술을 발견했습니다.",
    "그 여정은 미술관에서 끝났고, 나침반은 멈췄습니다.",
    "아름다운 그림들에 둘러싸여, 엠마는 예술가가 되고 싶다는 자신의 욕망을 깨달았습니다.",
    "영감을 받은 엠마는 집으로 돌아가 첫 번째 그림을 그리기 시작했고, 그 나침반은 이제 도시뿐 아니라 그녀의 꿈을 이끄는 가장 소중한 보물이 되었습니다."
]

# 탭 구성
st.title("II. Read with audio")
tab1, tab2, tab3 = st.tabs(["📖 Story", "🔤 Translation", "🔊 Read with audio"])

# 📖 본문 탭
with tab1:
    st.header("📖 Story")
    st.markdown(f"<div style='font-size: 18px; line-height: 1.6;'>{text.replace('\n', '<br>')}</div>", unsafe_allow_html=True)

# 🔤 해석 탭
with tab2:
    st.header("🔤 Translation")
    for i, trans in enumerate(translations, 1):
        st.markdown(f"<div style='font-size: 17px; margin-bottom: 8px;'><strong>{i}.</strong> {trans}</div>", unsafe_allow_html=True)

# 🔊 문장별 오디오 탭
with tab3:
    st.header("🔊 Select a sentence to hear")
    numbered_sentences = [f"{i+1}. {s}" for i, s in enumerate(sentences_raw)]
    selected = st.selectbox("Choose a sentence:", numbered_sentences)

    if st.button("Play Audio"):
        selected_index = numbered_sentences.index(selected)
        selected_sentence = sentences_raw[selected_index]
        st.write(f"**Selected sentence:** {selected_sentence}")

        tts = gTTS(text=selected_sentence, lang='en')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        st.audio(audio_bytes, format='audio/mp3')
