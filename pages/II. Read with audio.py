import streamlit as st
from gtts import gTTS
import io
import re

# 강조할 단어 목록 및 색상 스타일 설정
highlight_words = ["Emma", "compass", "desire", "journey", "gallery", "art"]
def highlight_text(text):
    for word in highlight_words:
        text = re.sub(f"\\b({word})\\b", r'<mark style="background-color: #fff59d;">\\1</mark>', text)
    return text

text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

translation = """
엠마는 어느 비 오는 오후 다락방에서 오래된 나침반을 발견했습니다. 그것은 단순한 나침반이 아니었습니다—자신의 가장 큰 욕망을 가리키는 나침반이었습니다. 호기심에 사로잡힌 엠마는 그 나침반을 따라, 전에 없던 방식으로 도시를 여행하게 됩니다.

나침반은 그녀를 외로운 헌책방, 인적이 끊긴 공원, 그리고 마침내 잊혀진 작은 미술관으로 이끌었습니다. 각 장소에서 엠마는 문학, 자연, 예술이라는 자신의 숨겨진 열정을 발견합니다. 미술관에 도착했을 때, 나침반은 멈추었습니다. 아름다운 그림들 속에서 엠마는 자신이 예술가가 되고 싶다는 욕망을 깨닫게 됩니다.

영감을 받은 엠마는 집으로 돌아가 첫 그림을 그리기 시작했고, 나침반은 이제 도시뿐만 아니라 그녀의 꿈을 안내해주는 가장 소중한 존재가 되었습니다.
"""

sentences = re.split(r'(?<=[.!?])\s+', text.strip())

st.title("II. Read with Audio")
tab1, tab2, tab3 = st.tabs(["1️⃣ 📖 Story", "2️⃣ ✏️ Translation", "3️⃣ 🔊 Read with audio"])

with tab1:
    st.header("Original Story")
    st.markdown(f"<div style='font-size:18px;'>{highlight_text(text)}</div>", unsafe_allow_html=True)

with tab2:
    st.header("한국어 해석")
    st.markdown(f"<div style='font-size:19px;'>{translation}</div>", unsafe_allow_html=True)

with tab3:
    st.header("Select a sentence to hear")

    # 문장 리스트를 번호와 함께 표시
    sentence_options = [f"{i+1}. {s}" for i, s in enumerate(sentences)]
    selected_label = st.selectbox("Choose a sentence:", sentence_options)
    selected_index = sentence_options.index(selected_label)
    selected_sentence = sentences[selected_index]

    if st.button("Play Audio"):
        st.markdown(f"**Selected sentence:** {selected_sentence}")

        # gTTS로 생성 (예외적으로 2, 5, 7번은 미리 녹음된 mp3 사용)
        if selected_index in [1, 4, 6]:
            st.audio(f"https://yourserver.com/audio/sentence_{selected_index+1}.mp3")
        else:
            tts = gTTS(text=selected_sentence, lang='en')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format='audio/mp3')

