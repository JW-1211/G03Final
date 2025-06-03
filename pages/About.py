import streamlit as st

st.title("About this app:")

st.markdown("""
Welcome to the **English Story Grammar and Vocabulary Analyzer**!

This application helps readers, learners, and educators better understand the grammar and vocabulary used in English stories.
""")

st.header("This application consists of:")
st.write("""

- **Overview**
- **Read with audio**
- **Vocabulary**
- **Grammar**
- **Thinking beyond**
""")

st.header("How It Works")
st.write("""
1. **Input your story text** into the application.
2. The app **processes the text** using natural language processing techniques.
3. It **displays grammar analysis**, including sentence parsing and parts of speech.
4. Vocabulary insights such as word frequency and difficulty levels are provided.
5. Interactive visualizations help you explore the structure and vocabulary of the story.
""")

st.header("Who Is This For?")
st.write("""
- Students learning English grammar and vocabulary  
- Teachers looking for tools to aid instruction  
- Writers and editors interested in language analysis  
- Anyone curious about the inner workings of English stories
""")

st.markdown("---")
st.write("Thank you for using our application! Feel free to explore and provide feedback.")
