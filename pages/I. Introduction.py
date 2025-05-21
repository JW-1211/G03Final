import streamlit as st
from PIL import Image

st.title("I. Introduction")

tab1, tab2 = st.tabs(["A four-panel summary of the story", "word cloud"])

with tab1:
    st.subheader("Story Summary")
    image = Image.open("images/Compass.png")
    st.image(image, caption="A four-panel comic", use_container_width=True)

with tab2:
    st.subheader("word cloud")
    image = Image.open("images/IMG_1605.jpeg")
    st.image(image, caption="", use_container_width=True)
