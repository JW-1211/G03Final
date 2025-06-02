# Lesson plan with customized apps

Prepared by Group 3

+ [Streamlit app link](https://g03final.streamlit.app)
+ [Github Code link](https://github.com/JW-1211/G03Final)

import streamlit as st

def introduction_page():
    st.title('Welcome to the English Story Grammar and Vocabulary Analyzer')
    
    st.header('Introduction')
    st.write(
        "This application helps you understand the grammar and vocabulary of English-based stories. "
        "It analyzes the text to provide insights into sentence structure, parts of speech, and vocabulary usage."
    )
    
    st.subheader('How to Use')
    st.write(
        "Simply input your English story text, and the application will process it to give you detailed grammatical and vocabulary analysis."
    )
    
    st.subheader('Features')
    st.write(
        "- Grammar analysis including sentence parsing and parts of speech tagging\n"
        "- Vocabulary insights such as word frequency and difficulty levels\n"
        "- Interactive visualization of sentence structures\n"
        "- Easy-to-understand summaries and explanations"
    )
    
    st.subheader('Get Started')
    st.write("To begin, navigate to the analysis page and enter your story text.")

# To display this page, call introduction_page() in your main Streamlit app
