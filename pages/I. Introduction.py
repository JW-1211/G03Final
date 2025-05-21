import streamlit as st
from PIL import Image

st.title("I. Introduction")

tab1, tab2 = st.tabs(["A four-panel summary of the story", "word cloud"])

with tab1:
    st.subheader("Story Summary")
    
    image1 = Image.open("images/Compass.png")
    image2 = Image.open("images/IMG_1605.jpeg")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption="A four-panel comic", use_container_width=True)
    with col2:
        st.image(image2, caption="Word cloud", use_container_width=True)

with tab2:
    st.subheader("guidelines")
    st.image(image, caption="guidelines", use_container_width=True)
