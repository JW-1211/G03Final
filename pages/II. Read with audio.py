import streamlit as st
from gtts import gTTS
import io
import re
import random

highlight_words = ["Emma", "compass", "desire", "journey", "gallery", "art"]

text_paragraphs = [
    "Emma found an old compass in her attic one rainy afternoon. It wasn’t just any compass—it pointed to one’s greatest desire rather than magnetic north. Emma, driven by curiosity, followed the compass’s lead, which took her on a journey through her city like never before.",
    "The compass led her to various places: a lonely old bookstore, a deserted park, and finally, a small, forgotten art gallery. At each stop, she discovered pieces of her own hidden passions: literature, nature, and art. The journey ended at the gallery, where the compass stopped moving. There, surrounded by beautiful paintings, Emma realized her desire to become an artist.",
    "Inspired, Emma went home to start her first painting, the compass now her most treasured possession, guiding her not just through the city, but through her dreams."
]

translation_paragraphs = [
    "엠마는 어느 비 오는 오후, 다락방에서 오래된 나침반을 발견했다. 그것은 단순한 나침반이 아니었다—자기 북이 아니라 가장 간절히 원하는 것을 가리켰다. 호기심에 이끌린 엠마는 나침반을 따라 전에는 몰랐던 방식으로 도시를 탐험하기 시작했다.",
    "나침반은 그녀를 외로운 헌책방, 인적 없는 공원, 그리고 마침내 잊혀진 작은 미술관으로 이끌었다. 각 장소에서 엠마는 자신의 숨겨진 열정—문학, 자연, 예술—을 발견했다. 여정은 미술관에서 끝났고, 나침반은 더 이상 움직이지 않았다. 아름다운 그림들로 둘러싸인 그곳에서, 엠마는 자신이 예술가가 되고 싶다는 바람을 깨달았다.",
    "영감을 받은 엠마는 집으로 돌아와 첫 그림을 그리기 시작했고, 나침반은 이제 도시뿐 아니라 그녀의 꿈을 안내하는 가장 소중한 보물이 되었다."
]

def highlight_keywords(text, keywords):
    for word in keywords:
        text = re.sub(rf'\b({word})\b', r'<mark style="background-color: #fff3b0">\1</mark>', text)
    return text

sentences = re.split(r'(?<=[.!?])\s+', ' '.join(text_paragraphs).strip())

st.title("II. Read with audio")

tab1, tab2, tab3 = st.tabs(["1️⃣ 📘 Story + Translation", "2️⃣ 🔊 Read with audio", "3️⃣ 🧩 Activity"])

with tab1:
    st.header("📘 Story + Translation")
    for eng, kor in zip(text_paragraphs, translation_paragraphs):
        st.markdown(f"<div style='font-size: 20px; line-height: 1.8; margin-bottom: 10px'>{highlight_keywords(eng, highlight_words)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 19px; line-height: 1.8; color: #555;'>{kor}</div>", unsafe_allow_html=True)
        st.markdown("---")

with tab2:
    st.header("🔊 Select a sentence to hear")
    sentence_options = [f"{i+1}. {s}" for i, s in enumerate(sentences)]
    selected = st.selectbox("Choose a sentence:", sentence_options)

    if st.button("▶️ Play Audio"):
        sentence_text = selected.split('. ', 1)[-1]
        tts = gTTS(text=sentence_text, lang='en')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes, format='audio/mp3')

with tab3:
    st.header("🧩 Story Activity: Select the correct order by number")
    st.markdown("📝 Read the sentences below, then select the correct order by choosing the numbers for each step.")

    correct_order = [
        "Emma found an old compass.",
        "Emma followed the compass through the city.",
        "Emma visited an art gallery.",
        "Emma decided to become an artist."
    ]

    # 번호와 문장 출력
    for idx, sentence in enumerate(correct_order, start=1):
        st.write(f"{idx}. {sentence}")

    step_keys = [f"step_{i}" for i in range(len(correct_order))]
    numbers = list(range(1, len(correct_order)+1))

    if 'selected_numbers' not in st.session_state:
        st.session_state.selected_numbers = {k: 0 for k in step_keys}  # 0 = not selected

    selected_numbers = st.session_state.selected_numbers

    # 중복 선택 방지용: 이미 고른 번호들
    chosen_numbers = [num for k, num in selected_numbers.items() if num != 0]

    for i, key in enumerate(step_keys):
        available_numbers = [num for num in numbers if num not in chosen_numbers or selected_numbers[key] == num]
        selected_num = st.selectbox(f"Step {i+1} 번호 선택", options=[0] + available_numbers, format_func=lambda x: "선택 안함" if x == 0 else str(x), key=key)
        selected_numbers[key] = selected_num
        # 선택 즉시 반영
        chosen_numbers = [num for k, num in selected_numbers.items() if num != 0]

    if st.button("Check Order"):
        user_order_nums = [selected_numbers[k] for k in step_keys]
        if 0 in user_order_nums:
            st.warning("모든 단계를 선택하세요.")
        elif len(set(user_order_nums)) != len(user_order_nums):
            st.warning("중복된 번호를 선택하지 마세요.")
        else:
            user_order = [correct_order[num - 1] for num in user_order_nums]
            if user_order == correct_order:
                st.success("✅ 정답입니다!")
            else:
                st.error("❌ 순서가 틀렸습니다. 다시 시도해보세요.")
