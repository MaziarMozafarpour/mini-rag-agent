from typing import override


from mini_rag.ingestion.document import Document
from mini_rag.ingestion.chunk import Chunk
from mini_rag.ingestion.chunkers.base import TextChunker


# -----------------------------------------------------------
class FixedSizeChunker(TextChunker):
    def __init__(self, chunk_size: int, chunk_overlap: int):
        if chunk_size <= 0:
            raise ValueError("chunk size must be greater than 0")

        if not 0 <= chunk_overlap < chunk_size:
            raise ValueError("invalid chunk overlap")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.step = chunk_size - chunk_overlap

    @override
    def chunk_document(self, document: Document) -> list[Chunk]:
        if len(document.content) == 0:
            return []

        chunks: list[Chunk] = []
        content_length = len(document.content)

        start = 0
        chunk_index = 0
        while start < content_length:
            end = start + self.chunk_size

            chunks.append(
                Chunk(
                    content=document.content[start:end],
                    metadata={
                        **document.metadata,
                        "chunk_index": chunk_index,
                    },
                )
            )

            if end >= content_length:
                break

            start += self.step
            chunk_index += 1

        return chunks
