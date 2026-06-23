"""
OJK AI Regulation Q&A — Streamlit Application
"""

import streamlit as st
import sys
sys.path.append("..")

from src.retrieval import hybrid_retrieve
from src.generation import generate_answer

st.set_page_config(
    page_title="OJK AI Regulation Q&A",
    page_icon="⚖️",
    layout="centered",
)

st.title("⚖️ OJK AI Regulation Q&A")
st.caption("Tanya jawab regulasi AI OJK & Bank Indonesia berbasis RAG")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Tanyakan tentang regulasi AI OJK..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mencari regulasi terkait..."):
            # TODO: wire up retrieval + generation
            response = "[TODO: implement RAG pipeline]"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
