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

tab1, tab2, tab3 = st.tabs(["1️⃣ 📘 Story + Translation", "2️⃣ 🔊 Read with audio", "3️⃣ 🧠 True / False Quiz"])

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
    st.header("🧠 True / False Quiz (Auto-generated)")
    st.markdown("아래 문장을 읽고 사실이면 ✅ True, 아니면 ❌ False를 선택하세요.")

    true_statements = [
        "Emma found an old compass.",
        "The compass pointed to her greatest desire.",
        "Emma followed the compass through the city.",
        "She visited a bookstore, a park, and an art gallery.",
        "The compass stopped moving in the gallery.",
        "Emma realized she wanted to become an artist.",
        "Emma started painting after the journey."
    ]

    false_versions = {
        "Emma found an old compass.": "Emma found an old **map**.",
        "The compass pointed to her greatest desire.": "The compass pointed to **magnetic north**.",
        "Emma followed the compass through the city.": "Emma **ignored** the compass and stayed home.",
        "She visited a bookstore, a park, and an art gallery.": "She visited a **café**, a mall, and a theater.",
        "The compass stopped moving in the gallery.": "The compass **never stopped** moving.",
        "Emma realized she wanted to become an artist.": "Emma realized she wanted to become a **scientist**.",
        "Emma started painting after the journey.": "Emma started **writing poems** after the journey."
    }

    # 새 문제 만들기 버튼
    if st.button("🔁 새 문제 풀기"):
        if 'quiz_items' in st.session_state:
            del st.session_state.quiz_items

    # 문제 생성
    if 'quiz_items' not in st.session_state:
        selected_true = random.sample(true_statements, 2)
        selected_false = random.sample([false_versions[s] for s in selected_true], 2)
        quiz_items = [(s, True) for s in selected_true] + [(s, False) for s in selected_false]
        random.shuffle(quiz_items)
        st.session_state.quiz_items = quiz_items
    else:
        quiz_items = st.session_state.quiz_items

    user_answers = []
    for i, (question, _) in enumerate(quiz_items):
        user_input = st.radio(f"{i+1}. {question}", options=["True", "False"], key=f"tf_{i}")
        user_answers.append(user_input == "True")

    if st.button("Check Answers"):
        score = 0
        for i, (q, correct) in enumerate(quiz_items):
            if user_answers[i] == correct:
                st.success(f"✅ Q{i+1}: Correct")
                score += 1
            else:
                st.error(f"❌ Q{i+1}: Incorrect (Answer: {'True' if correct else 'False'})")
        st.markdown(f"### Your Score: {score} / {len(quiz_items)}")

    if st.button("📖 해설 보기"):
        st.markdown("### 📘 해설")
        for i, (q, correct) in enumerate(quiz_items):
            explanation = "This is stated in the story." if correct else "This is **not** mentioned or contradicts the story."
            st.markdown(f"**Q{i+1}:** {q} → {'✅ True' if correct else '❌ False'}  \n→ {explanation}")
