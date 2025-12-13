import streamlit as st
from pdf_utils import extract_page_text
from search_utils import search_sentences

st.set_page_config(page_title="PDF Sentence Search", layout="wide")

st.title("📄 PDF Search – Sentence Finder")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

search_text = st.text_input("Enter word / phrase to search")

search_mode = st.radio(
    "Search Mode",
    ["Exact Phrase", "Group of Words"],
    horizontal=True
)

if uploaded_file and search_text:
    with st.spinner("Reading PDF..."):
        pages_data = extract_page_text(uploaded_file)

    mode = "phrase" if search_mode == "Exact Phrase" else "words"

    with st.spinner("Searching..."):
        results = search_sentences(pages_data, search_text, mode)

    st.success(f"Found {len(results)} matching sentence(s)")

    if results:
        for res in results:
            st.markdown(
                f"""
                **📄 Page {res['page']}**  
                {res['sentence']}
                ---
                """
            )
    else:
        st.warning("No matching sentences found.")