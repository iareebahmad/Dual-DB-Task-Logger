import streamlit as st
import webbrowser

st.title("Dual Database Task Logger")
st.header("Please choose your preferred Database")

db = st.selectbox("Choose your Database : ",["Select an Option","SQLite3","PostgreSQL"])
urls = {"SQLite3": "https://github.com","PostgreSQL": "https://youtube.com"}

# Button to trigger redirection
if st.button("Use this Database"):
    if db != "Select an option":
        st.success(f"Opening {db} Database Task Logger")
        webbrowser.open_new_tab(urls[db])
    else:
        st.warning("Please select a website first.")