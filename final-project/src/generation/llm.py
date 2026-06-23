"""LLM client wrapper supporting OpenAI and Ollama (open-source)."""


def generate_answer(question: str, context: str, provider: str = "openai", model: str = "gpt-4o") -> str:
    """Generate an answer given a question and retrieved context.
    
    Args:
        question: User's question.
        context: Retrieved regulatory document chunks.
        provider: 'openai' or 'ollama'.
        model: Model name.
    """
    # TODO: implement with openai / ollama client
    raise NotImplementedError
