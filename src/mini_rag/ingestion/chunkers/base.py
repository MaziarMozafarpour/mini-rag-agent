from abc import ABC, abstractmethod


from mini_rag.ingestion.chunk import Chunk
from mini_rag.ingestion.document import Document


class TextChunker(ABC):
    @abstractmethod
    def chunk_document(self, document: Document) -> list[Chunk]: ...
