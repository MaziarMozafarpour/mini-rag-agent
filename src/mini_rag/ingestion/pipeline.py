from pathlib import Path

from mini_rag.ingestion.loaders.base import DocumentLoader
from mini_rag.ingestion.chunkers.base import TextChunker
from mini_rag.ingestion.chunk import Chunk


class DocumentIngestionPipeline:
    def __init__(self, loader: DocumentLoader, chunker: TextChunker):
        if not isinstance(loader, DocumentLoader):
            raise TypeError("loader must be type of DocumentLoader")
        if not isinstance(chunker, TextChunker):
            raise TypeError("chunker must be type of TextChunker")

        self.loader = loader
        self.chunker = chunker

    def ingest(self, path: Path) -> list[Chunk]:
        try:
            document = self.loader.load_document(path=path)
            chunks = self.chunker.chunk_document(document=document)
            return chunks
        except Exception as e:
            raise e
