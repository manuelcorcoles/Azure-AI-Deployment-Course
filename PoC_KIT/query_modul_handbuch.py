import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


DEFAULT_VECTOR_STORE_NAME = "modul_handbuch_pages"


def get_openai_client():
    load_dotenv()
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not azure_openai_endpoint:
        raise EnvironmentError(
            "AZURE_OPENAI_ENDPOINT is not set in your environment or .env file."
        )

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )

    return OpenAI(base_url=azure_openai_endpoint, api_key=token_provider)


def find_vector_store(client, name):
    for page in client.vector_stores.list(limit=100):
        if getattr(page, "name", None) == name:
            return page
    return None


def ask_question(client, vector_store_id, model, question):
    response = client.responses.create(
        model=model,
        instructions=(
            "You are a module retrieval assistant for the KIT Informatik Master modulhandbuch. "
            "Use the provided document fragments from the vector store to answer questions about modules, "
            "course descriptions, and relevant program details. "
            "Cite page-based facts from the modulhandbuch when they are available."
        ),
        input=question,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [vector_store_id],
            }
        ],
    )

    return response


def parse_args():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Ask a question using the modulhandbuch vector store."
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_DEPLOYMENT"),
        help="Azure OpenAI deployment name to use for responses. If omitted, MODEL_DEPLOYMENT from .env is used.",
    )
    parser.add_argument(
        "--vector-store",
        default=DEFAULT_VECTOR_STORE_NAME,
        help="Name of the vector store containing modulhandbuch page chunks.",
    )
    parser.add_argument(
        "--question",
        help="A single question to ask. If omitted, the script enters interactive mode.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.model:
        raise ValueError(
            "MODEL_DEPLOYMENT is not set. Provide --model or set MODEL_DEPLOYMENT in .env."
        )

    client = get_openai_client()
    vector_store = find_vector_store(client, args.vector_store)
    if vector_store is None:
        raise RuntimeError(
            f"Vector store '{args.vector_store}' was not found. "
            "Run the ingestion script first."
        )

    if args.question:
        question = args.question.strip()
        if not question:
            raise ValueError("Question cannot be empty.")
        response = ask_question(client, vector_store.id, args.model, question)
        print(response.output_text)
        return

    print("Enter a question about the modulhandbuch. Type 'quit' or 'exit' to stop.")
    while True:
        question = input("Question: ").strip()
        if not question:
            continue
        if question.lower() in {"quit", "exit"}:
            break

        response = ask_question(client, vector_store.id, args.model, question)
        print("\nAnswer:\n")
        print(response.output_text)
        print("\n---\n")


if __name__ == "__main__":
    main()
