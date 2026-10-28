from typing import override
from pathlib import Path

from mini_rag.ingestion.document import Document
from mini_rag.ingestion.loaders.base import DocumentLoader


# -----------------------------------------------------------
class MarkdownDocumentLoader(DocumentLoader):
    @override
    def load_document(self, path: Path) -> Document:
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        if path.suffix.lower() != ".md":
            raise ValueError("File must have a .md extension")

        content = path.read_text(encoding="utf-8")

        metadata = {
            "filename": path.name,
            "extension": path.suffix,
            "source": str(path.resolve()),
            "file_size": path.stat().st_size,
        }

        return Document(content=content, metadata=metadata)
