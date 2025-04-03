import json
from typing import Any, Dict, Type

from agno.document.chunking.recursive import RecursiveChunking
from agno.document.chunking.strategy import ChunkingStrategy


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles special objects."""

    def default(self, obj: Any) -> Any:
        # Handle RecursiveChunking objects
        if isinstance(obj, RecursiveChunking):
            return {
                "__type__": "RecursiveChunking",
                "chunk_size": getattr(obj, "chunk_size", 3000),
                "chunk_overlap": getattr(obj, "chunk_overlap", 0),
                "separators": getattr(obj, "separators", ["\n", " "])
            }
        # Handle other non-serializable objects in the knowledge base
        if isinstance(obj, ChunkingStrategy):
            return {
                "__type__": obj.__class__.__name__,
                "params": str(obj)
            }
        # Handle other complex objects that have a __dict__
        if hasattr(obj, "__dict__"):
            return {
                "__type__": obj.__class__.__name__,
                "module": obj.__class__.__module__,
                "is_object": True
            }
        return super().default(obj)


def custom_serialize(obj: Any) -> str:
    """Serialize an object to JSON string using the custom encoder."""
    return json.dumps(obj, cls=CustomJSONEncoder)
