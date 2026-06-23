#!/usr/bin/env python3
"""
rag_helper.py - Adapted from DataTalksClub/llm-zoomcamp rag_helper.py

Changes from original:
- search()       : removed FAQ boost/filter, uses filename/content schema
- build_context(): uses filename + content fields instead of section/question/answer
- llm()          : uses chat.completions.create (OpenRouter-compatible) instead of
                   responses.create; returns full response object for token tracking
- rag()          : returns (answer, usage) tuple instead of plain string
"""

from dataclasses import dataclass

INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()


@dataclass
class RAGResult:
    """Container for RAG response with token usage."""
    answer: str
    input_tokens: int
    output_tokens: int


class RAGBase:

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model='openai/gpt-4.1-mini',  # gpt-5.4-mini via OpenRouter
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query, num_results=5):
        """Search using filename/content schema (no FAQ boost/filter)."""
        return self.index.search(query, num_results=num_results)

    def build_context(self, search_results):
        """Build context from filename + content fields."""
        lines = []
        for doc in search_results:
            lines.append(f"## {doc['filename']}")
            lines.append(doc['content'])
            lines.append('')
        return '\n'.join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )

    def llm(self, prompt):
        """Call LLM via chat.completions (OpenRouter-compatible). Returns full response."""
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self.instructions},
                {'role': 'user', 'content': prompt},
            ],
        )
        return response

    def rag(self, query) -> RAGResult:
        """Run full RAG pipeline. Returns RAGResult with answer + token usage."""
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        response = self.llm(prompt)
        return RAGResult(
            answer=response.choices[0].message.content,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
        )
