"""Streamlit application for the OJK Regulatory Intelligence Assistant."""
import streamlit as st

st.set_page_config(
    page_title="OJK Regulatory Intelligence Assistant",
    page_icon="⚖️",
    layout="wide",
)

st.title("⚖️ OJK Regulatory Intelligence Assistant")
st.caption("Ask questions about OJK and Bank Indonesia regulations")

# TODO: Implement full RAG UI
query = st.text_input("Enter your regulatory question:", placeholder="e.g., What are the capital requirements for digital banks under POJK 12?")

if query:
    st.info("🚧 RAG pipeline not yet connected. Implement src/ modules first.")
