import streamlit as st
st.title("I. Introduction")
tab1, tab2 = st.tabs(["A four-panel summary of the story" , "..."])
with tab1:
    st.write("First")
with tab2:
    st.write("Second")
