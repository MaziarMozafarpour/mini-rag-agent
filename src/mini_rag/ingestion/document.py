from typing import Any


class Document:
    def __init__(self, content: str, metadata: dict[str, Any] | None = None) -> None:
        if not isinstance(content, str):
            raise TypeError("Document content must be a string")

        self.content = content
        self.metadata = metadata.copy() if metadata else {}
