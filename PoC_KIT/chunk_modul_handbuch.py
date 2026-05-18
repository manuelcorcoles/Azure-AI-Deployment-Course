import json
from pathlib import Path


PDF_PATH = Path(__file__).parent / "modul_handbuch.pdf"
OUTPUT_DIR = Path(__file__).parent / "page_chunks"
OUTPUT_FILE = Path(__file__).parent / "modul_handbuch_pages.json"


def extract_pages(pdf_path):
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError(
            "PyPDF2 is not installed. Install it with: python -m pip install PyPDF2"
        )

    reader = PdfReader(pdf_path)
    for page_index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        yield {
            "id": f"{pdf_path.stem}-page-{page_index}",
            "text": text.strip(),
            "metadata": {
                "page": page_index,
                "source": pdf_path.name,
            },
        }


def main():
    if not PDF_PATH.exists():
        print(f"PDF file not found: {PDF_PATH}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Extracting pages from {PDF_PATH.name}...")
    page_list = [page_data for page_data in extract_pages(PDF_PATH)]
    with OUTPUT_FILE.open("w", encoding="utf-8") as output_stream:
        json.dump(page_list, output_stream, ensure_ascii=False, indent=2)

    print(f"Saved page chunks to: {OUTPUT_FILE}")
    print("Saved a JSON array of page chunks with fields: id, text, metadata")


if __name__ == "__main__":
    main()
