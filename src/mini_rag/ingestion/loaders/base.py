from pathlib import Path
from abc import ABC, abstractmethod

from mini_rag.ingestion.document import Document


class DocumentLoader(ABC):
    @abstractmethod
    def load_document(self, path: Path) -> Document: ...
