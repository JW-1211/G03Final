import streamlit as st
from PIL import Image

st.title("I. Introduction")

# 탭 2개 생성
tab1, tab2 = st.tabs(["A four-panel summary of the story", "Word cloud"])

with tab1:
    st.subheader("Story Summary")

    col1, col2 = st.columns(2)

    with col1:
        image1 = Image.open("images/Compass.png")
        st.image(image1, caption="A four-panel comic", use_container_width=True)

    with col2:
        image2 = Image.open("images/IMG_1605.jpeg")
        st.image(image2, caption="Word cloud", use_container_width=True)

with tab2:
    st.subheader("guidelines")
    st.write("This tab does not contain an image.")
