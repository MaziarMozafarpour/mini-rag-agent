import pytest

from mini_rag.ingestion.document import Document
from mini_rag.ingestion.chunkers.fixed_size import FixedSizeChunker


@pytest.mark.parametrize(
    ("content", "chunk_size", "chunk_overlap", "expected"),
    [
        ("", 6, 2, []),
        ("ABC", 6, 2, ["ABC"]),
        ("ABCDEF", 6, 2, ["ABCDEF"]),
        ("ABCDEFGHIJ", 5, 0, ["ABCDE", "FGHIJ"]),
        ("ABCDEFG", 3, 2, ["ABC", "BCD", "CDE", "DEF", "EFG"]),
        ("ABCDEFGHIJK", 6, 2, ["ABCDEF", "EFGHIJ", "IJK"]),
    ],
)
def test_fixed_size_chunker_edge_cases(
    content: str,
    chunk_size: int,
    chunk_overlap: int,
    expected: list[str],
):
    document = Document(content=content)
    chunker = FixedSizeChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = chunker.chunk_document(document)

    assert [chunk.content for chunk in chunks] == expected


@pytest.mark.parametrize("chunk_size", [0, -1, -10])
def test_fixed_size_chunker_rejects_invalid_chunk_size(chunk_size: int):
    with pytest.raises(ValueError):
        FixedSizeChunker(chunk_size=chunk_size, chunk_overlap=0)


@pytest.mark.parametrize("chunk_overlap", [-1, 5, 6, 10])
def test_fixed_size_chunker_rejects_invalid_overlap(chunk_overlap: int):
    with pytest.raises(ValueError):
        FixedSizeChunker(chunk_size=5, chunk_overlap=chunk_overlap)


def test_fixed_size_chunker_preserves_document_metadata():
    document = Document(
        content="ABCDEFGHIJ",
        metadata={"source": "test.md", "author": "Maziar"},
    )
    chunker = FixedSizeChunker(chunk_size=5, chunk_overlap=2)

    chunks = chunker.chunk_document(document)

    for chunk in chunks:
        assert document.metadata.items() <= chunk.metadata.items()


def test_fixed_size_chunker_assigns_sequential_chunk_indices():
    document = Document(content="ABCDEFGHIJKLMNO")
    chunker = FixedSizeChunker(chunk_size=6, chunk_overlap=2)

    chunks = chunker.chunk_document(document)

    assert [chunk.metadata["chunk_index"] for chunk in chunks] == list(
        range(len(chunks))
    )


def test_fixed_size_chunker_does_not_mutate_document_metadata():
    original_metadata = {"source": "test.md", "author": "Maziar"}
    document = Document(
        content="ABCDEFGHIJ",
        metadata=original_metadata,
    )
    chunker = FixedSizeChunker(chunk_size=5, chunk_overlap=2)

    chunker.chunk_document(document)

    assert document.metadata == original_metadata
    assert "chunk_index" not in document.metadata
