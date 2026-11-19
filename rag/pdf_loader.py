from pathlib import Path
import pymupdf


def load_pdf(file_path):
    pages = []
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        with pymupdf.open(file_path) as doc:
            for page_number, page in enumerate(doc, start=1):
                text = page.get_text("text").strip()

                if not text:
                    continue

                pages.append({
                    "document": file_path.name,
                    "page": page_number,
                    "text": text
                })

    except (pymupdf.FileDataError, pymupdf.EmptyFileError) as e:
        raise ValueError(f"Не удалось прочитать PDF: {e}") from e

    if not pages:
        raise ValueError("В PDF не найден извлекаемый текст")

    return pages