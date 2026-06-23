"""Evaluate RAG system quality using hit rate, MRR, and LLM-as-judge."""

from typing import List, Dict, Callable


def hit_rate(ground_truth: List[Dict], retrieval_fn: Callable, top_k: int = 5) -> float:
    """Calculate hit rate: fraction of queries where the correct doc is in top-k results."""
    hits = 0
    for item in ground_truth:
        results = retrieval_fn(item["question"])
        retrieved_ids = [r.get("doc_id") for r in results[:top_k]]
        if item["doc_id"] in retrieved_ids:
            hits += 1
    return hits / len(ground_truth)


def mean_reciprocal_rank(ground_truth: List[Dict], retrieval_fn: Callable, top_k: int = 5) -> float:
    """Calculate MRR: mean of reciprocal ranks of correct documents."""
    rr_sum = 0.0
    for item in ground_truth:
        results = retrieval_fn(item["question"])
        retrieved_ids = [r.get("doc_id") for r in results[:top_k]]
        if item["doc_id"] in retrieved_ids:
            rank = retrieved_ids.index(item["doc_id"]) + 1
            rr_sum += 1 / rank
    return rr_sum / len(ground_truth)


def llm_judge_score(question: str, answer: str, context: str, llm_client) -> Dict:
    """Use LLM to evaluate answer quality."""
    from generation.prompts import EVALUATION_PROMPT
    import json
    prompt = EVALUATION_PROMPT.format(question=question, context=context, answer=answer)
    response = llm_client.generate(
        system_prompt="Anda adalah evaluator kualitas jawaban AI.",
        user_prompt=prompt
    )
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"score": 0, "reason": "parse error"}
