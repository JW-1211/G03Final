import streamlit as st
from PIL import Image

st.title("I. Introduction")

tab1, tab2 = st.tabs(["💫Guess the story", "💫Guidelines"])

with tab1:
    st.subheader("Guess the story")
    st.write("Let's guess the story!")

    col1, col2 = st.columns(2)

    with col1:
        image1 = Image.open("images/Compass.png")
        st.image(image1, caption="A four-panel comic", use_container_width=True)

    with col2:
        image2 = Image.open("images/IMG_1605.jpeg")
        st.image(image2, caption="Word cloud", use_container_width=True)

with tab2:
    st.subheader("Guidelines")
    st.write("""
Let’s try to guess the overall flow of the story based on the four-panel comic.

Let’s try to predict the key words that appear in the story using the word cloud.

So, what might happen to the main character?
""")
