from pathlib import Path

import pytest

from mini_rag.ingestion.document import Document
from mini_rag.ingestion.loaders.markdown import MarkdownDocumentLoader


def test_load_document_returns_content_and_metadata(tmp_path: Path) -> None:
    content = "# Hello Test"
    file_path = tmp_path / "valid.md"
    file_path.write_text(content, encoding="utf-8")

    loader = MarkdownDocumentLoader()

    document = loader.load_document(file_path)

    assert isinstance(document, Document)
    assert document.content == content
    assert document.metadata == {
        "filename": "valid.md",
        "extension": ".md",
        "source": str(file_path.resolve()),
        "file_size": file_path.stat().st_size,
    }


@pytest.mark.parametrize("extension", [".MD", ".Md", ".mD"])
def test_load_document_accepts_case_insensitive_extensions(
    tmp_path: Path, extension: str
) -> None:
    file_path = tmp_path / f"document{extension}"
    file_path.write_text("# Hello", encoding="utf-8")

    loader = MarkdownDocumentLoader()

    document = loader.load_document(file_path)

    assert document.content == "# Hello"
    assert document.metadata["extension"] == extension


def test_load_document_raises_error_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "missing.md"
    loader = MarkdownDocumentLoader()

    with pytest.raises(FileNotFoundError, match=f"File does not exist: {file_path}"):
        loader.load_document(file_path)


def test_load_document_rejects_invalid_extension(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "document.txt"
    file_path.write_text("Some content", encoding="utf-8")

    loader = MarkdownDocumentLoader()

    with pytest.raises(ValueError, match="File must have a .md extension"):
        loader.load_document(file_path)


def test_load_document_rejects_directory(tmp_path: Path) -> None:
    loader = MarkdownDocumentLoader()

    with pytest.raises(ValueError, match=f"Path is not a file: {tmp_path}"):
        loader.load_document(tmp_path)


def test_load_document_accepts_empty_file(tmp_path: Path) -> None:
    file_path = tmp_path / "empty.md"
    file_path.write_text("", encoding="utf-8")

    loader = MarkdownDocumentLoader()

    document = loader.load_document(file_path)

    assert isinstance(document, Document)
    assert document.content == ""
    assert document.metadata["file_size"] == 0


def test_load_document_raises_error_for_invalid_utf8(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "invalid.md"
    file_path.write_bytes(b"\xff\xfe\xfa")

    loader = MarkdownDocumentLoader()

    with pytest.raises(UnicodeDecodeError):
        loader.load_document(file_path)
