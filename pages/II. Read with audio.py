import streamlit as st
from gtts import gTTS
import io
import re

text = """
Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.

The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.

Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams.
"""

translation = """
엠마는 어느 비 오는 오후, 다락방에서 오래된 나침반을 발견했습니다. 그것은 평범한 나침반이 아니었습니다—북쪽이 아니라 사람의 가장 큰 욕망을 가리켰습니다. 엠마는 호기심에 이끌려 나침반이 가리키는 방향을 따라갔고, 전혀 새로운 방식으로 도시를 여행하게 되었습니다.

나침반은 그녀를 외로운 오래된 서점, 버려진 공원, 그리고 마침내 작은 잊혀진 미술관으로 이끌었습니다. 각 장소에서 그녀는 자신의 숨겨진 열정인 문학, 자연, 예술을 발견했습니다. 여정은 미술관에서 끝났고, 나침반은 멈췄습니다. 아름다운 그림들에 둘러싸여, 엠마는 자신이 예술가가 되고 싶다는 열망을 깨달았습니다.

영감을 받은 엠마는 집으로 돌아가 첫 그림을 그리기 시작했고, 그 나침반은 이제 그녀의 가장 소중한 소지품이자 도시의 길만이 아니라 꿈을 향한 안내자가 되었습니다.
"""

highlight_words = ["compass", "desire", "Emma", "journey", "gallery", "art"]

def highlight_text(text, words):
    for word in words:
        pattern = re.compile(rf'\b({word})\b', re.IGNORECASE)
        text = pattern.sub(
            r'<span style="background-color: rgba(255, 255, 0, 0.3); padding: 2px 4px; border-radius: 4px;">\1</span>',
            text
        )
    return text

sentences = re.split(r'(?<=[.!?])\s+', text.strip())

st.title("II. Read with audio")

tab1, tab2, tab3 = st.tabs(["📖 1. Story", "🔤 2. Translation", "🔊 3. Read with audio"])

with tab1:
    st.header("📖 Story")
    highlighted_text = highlight_text(text, highlight_words)
    st.markdown(
        f"<div style='font-size: 20px; line-height: 1.8;'>{highlighted_text.replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True
    )

with tab2:
    st.header("🔤 Translation")
    st.markdown(
        f"<div style='font-size: 18px; line-height: 1.8;'>{translation.replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True
    )

with tab3:
    st.header("🔊 Select a sentence to hear")
    numbered_sentences = [f"{i+1}. {s}" for i, s in enumerate(sentences)]
    selected = st.selectbox("Choose a sentence:", numbered_sentences)

    if st.button("▶️ Play Audio"):
        selected_sentence = re.sub(r'^\d+\.\s+', '', selected)
        st.write(f"**Selected sentence:** {selected_sentence}")

        tts = gTTS(text=selected_sentence, lang='en')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        st.audio(audio_bytes, format='audio/mp3')
