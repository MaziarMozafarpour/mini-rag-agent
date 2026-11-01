from typing import Any


# -----------------------------------------------------------
class Chunk:
    def __init__(self, content: str, metadata: dict[str, Any] | None = None):
        if not isinstance(content, str):
            raise TypeError("Chunk content must be a string")
        self.content = content
        self.metadata = metadata.copy() if metadata else {}
