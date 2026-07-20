from dotenv import load_dotenv

load_dotenv()

from agent import faq_agent, SearchDeps
from ingest import build_index, load_faq_data
import logfire
logfire.configure()
logfire.instrument_pydantic_ai()

def main():
    # Download the FAQ and build the search index
    documents = load_faq_data()
    index = build_index(documents)

    # Inject the index into the agent via the dependency container
    deps = SearchDeps(index=index)

    # Ask a question
    question = 'How do I run Ollama locally?'
    result = faq_agent.run_sync(question, deps=deps)

    print(result.output)


if __name__ == '__main__':
    main()
