import streamlit as st
from PIL import Image

st.title("I. Overview")

tab1, tab2, tab3 = st.tabs(["🧭 Guidelines", "🧩 Guess the story", "🗣️ Share ideas"])

with tab1:
    st.subheader("Guidelines")
    st.write("""
    
    <Before we start today’s lesson, let’s guess what the story is about!>
    
1.  Let’s try to guess the overall flow of the story based on the **four-panel comic picture**.

2.  Let’s try to predict the key words that appear in the story using the **word cloud**.

3. What do you think will happen to the main character? **Talk in your group!**

""")


with tab2:
    st.subheader("Guess the story")
    st.write("Let's guess the story!")
    
    col1, col2 = st.columns(2)

    with col1:
        image1 = Image.open("images/CompassNumber.jpg")
        st.image(image1, caption="A four-panel comic picture", use_container_width=True)

    with col2:
        image2 = Image.open("images/IMG_1605.jpeg")
        st.image(image2, caption="Word cloud", use_container_width=True)
