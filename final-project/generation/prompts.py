"""Prompt templates for OJK regulatory Q&A."""

RAG_SYSTEM_PROMPT = """Anda adalah asisten hukum keuangan yang ahli dalam regulasi OJK (Otoritas Jasa Keuangan) dan Bank Indonesia.
Jawab pertanyaan berdasarkan konteks regulasi yang diberikan.
Jika informasi tidak tersedia dalam konteks, sampaikan dengan jelas bahwa Anda tidak memiliki informasi tersebut.
Gunakan bahasa yang formal dan tepat sesuai konteks regulasi keuangan Indonesia."""

RAG_USER_TEMPLATE = """Konteks Regulasi:
{context}

Pertanyaan: {question}

Berikan jawaban yang akurat dan ringkas berdasarkan konteks di atas."""

EVALUATION_PROMPT = """Evaluasi kualitas jawaban berikut berdasarkan pertanyaan dan konteks yang diberikan.

Pertanyaan: {question}
Konteks: {context}
Jawaban yang diberikan: {answer}

Berikan skor dari 1-5 dan penjelasan singkat.
Format: {{"score": <1-5>, "reason": "<alasan>"}}"""


def build_rag_prompt(question: str, context_docs: list) -> str:
    """Build the RAG prompt from question and retrieved documents."""
    context = "\n\n".join([
        f"[{doc.get('source', 'Regulasi')}] {doc.get('content', '')}"
        for doc in context_docs
    ])
    return RAG_USER_TEMPLATE.format(context=context, question=question)
