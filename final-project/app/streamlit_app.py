"""Streamlit UI for OJK Regulatory Q&A Assistant."""

import streamlit as st

st.set_page_config(
    page_title="OJK Regulatory Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ OJK Regulatory Q&A Assistant")
st.markdown("""
Ask questions about **OJK** and **Bank Indonesia** regulations in natural language.
> _Powered by RAG (Retrieval-Augmented Generation)_
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    llm_provider = st.selectbox("LLM Provider", ["OpenAI (GPT-4o-mini)", "Ollama (Llama 3)"])
    top_k = st.slider("Top-K Documents", 1, 10, 5)
    search_mode = st.radio("Search Mode", ["Hybrid (BM25 + Vector)", "Vector Only", "BM25 Only"])

# Main Q&A interface
question = st.text_input(
    "Ask a regulatory question:",
    placeholder="e.g. Apa persyaratan modal minimum untuk bank umum menurut POJK?"
)

if st.button("Search", type="primary") and question:
    with st.spinner("Retrieving relevant regulations..."):
        st.info("🔍 Searching regulatory documents...")
        # TODO: wire up retrieval pipeline
        st.warning("⚠️ Ingestion pipeline not yet initialized. Please run `python ingestion/indexing.py` first.")

# Footer
st.divider()
st.caption("Data source: OJK POJK, SEOJK, and Bank Indonesia circulars.")
