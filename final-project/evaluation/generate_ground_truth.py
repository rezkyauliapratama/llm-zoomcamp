"""Generate ground-truth Q&A pairs from regulatory documents for evaluation."""

from typing import List, Dict


def generate_qa_pairs(documents: List[Dict], llm_client, num_questions: int = 5) -> List[Dict]:
    """Use LLM to generate Q&A pairs from regulatory document chunks."""
    qa_pairs = []
    for doc in documents:
        prompt = f"""Berdasarkan teks regulasi berikut, buat {num_questions} pertanyaan dan jawaban.
Teks: {doc['content']}

Format JSON:
[{{"question": "...", "answer": "...", "doc_id": "{doc.get('doc_id', '')}"}}, ...]"""
        response = llm_client.generate(
            system_prompt="Anda adalah ahli regulasi keuangan Indonesia.",
            user_prompt=prompt
        )
        import json
        try:
            pairs = json.loads(response)
            qa_pairs.extend(pairs)
        except json.JSONDecodeError:
            print(f"Failed to parse QA pairs for doc {doc.get('doc_id')}")
    return qa_pairs
