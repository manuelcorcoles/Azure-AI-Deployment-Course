import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


DEFAULT_VECTOR_STORE_NAME = "modul_handbuch_pages"
JSON_FILE = Path(__file__).parent / "modul_handbuch_pages.json"


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


def create_vector_store(client, name):
    print(f"Creating vector store '{name}'...")
    return client.vector_stores.create(name=name)


def ingest_json_file(client, vector_store_id, json_path):
    if not json_path.exists():
        raise FileNotFoundError(
            f"Chunk file not found: {json_path}\n"
            "Run PoC_KIT/chunk_modul_handbuch.py first to generate it."
        )

    with json_path.open("rb") as json_stream:
        file_batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=[json_stream],
        )

    return file_batch


def parse_args():
    parser = argparse.ArgumentParser(
        description="Upload modul_handbuch page chunks into an Azure OpenAI vector store."
    )
    parser.add_argument(
        "--name",
        default=DEFAULT_VECTOR_STORE_NAME,
        help="Vector store name to create or reuse.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete and recreate the vector store if it already exists.",
    )
    parser.add_argument(
        "--file",
        default=str(JSON_FILE),
        help="Path to the JSON chunk file.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    client = get_openai_client()
    jsonl_path = Path(args.file)

    if args.replace:
        existing = find_vector_store(client, args.name)
        if existing:
            print(f"Found existing vector store '{args.name}' (id={existing.id}). Replacing it...")
            client.vector_stores.delete(existing.id)
            existing = None

    vector_store = find_vector_store(client, args.name)
    if vector_store is None:
        vector_store = create_vector_store(client, args.name)
    else:
        print(f"Reusing existing vector store '{args.name}' (id={vector_store.id}).")

    file_batch = ingest_json_file(client, vector_store.id, jsonl_path)

    print("\nIngestion complete.")
    print(f"Vector store id: {vector_store.id}")
    print(f"Files uploaded: {file_batch.file_counts.completed}")
    print("You can now query this store with the OpenAI Responses API and file_search tool.")


if __name__ == "__main__":
    main()
