import streamlit as st
from PIL import Image

st.title("I. Introduction")

tab1, tab2 = st.tabs(["A four-panel summary of the story", "..."])

with tab1:
    st.subheader("Story Summary")
    image = Image.open("images/Compass.png")
    st.image(image, caption="A four-panel comic", use_container_width=True)

with tab2:
    st.write("Second tab content here.")
