"""Generate synthetic Q&A pairs from OJK/BI regulatory chunks for evaluation.

Process:
    For each chunk (pasal text), use LLM to generate 2-3 questions
    that require reading that pasal to answer.

Output:
    evaluation/data/eval_questions.csv
    Columns: question, expected_answer, source_document, pasal
"""

import csv
from pathlib import Path

GROUND_TRUTH_PROMPT = """Given the following regulatory document excerpt, generate {n_questions} questions
that can ONLY be answered by reading this specific text. Questions should be natural
business/compliance questions a banker would ask.

Document: {source_document}
Passage: {pasal}
Text:
{content}

Output as JSON: [{"question": "...", "answer": "..."}]"""

OUTPUT_PATH = Path(__file__).parent / "data" / "eval_questions.csv"


def generate_qa_pairs(chunks: list[dict], n_questions: int = 2, llm_client=None) -> list[dict]:
    """Generate Q&A pairs from document chunks."""
    # TODO: Implement LLM-based Q&A generation
    raise NotImplementedError("Ground truth generation pending")


def save_ground_truth(qa_pairs: list[dict], output_path: Path = OUTPUT_PATH) -> None:
    """Save Q&A pairs to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["question", "expected_answer", "source_document", "pasal"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(qa_pairs)
    print(f"Saved {len(qa_pairs)} Q&A pairs to {output_path}")
