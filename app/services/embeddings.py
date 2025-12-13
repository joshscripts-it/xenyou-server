from typing import List
import os

from sentence_transformers import SentenceTransformer

_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
_MODEL = SentenceTransformer(_MODEL_NAME)


def get_embedding(text: str) -> List[float]:
    emb = _MODEL.encode([text], show_progress_bar=False)[0]
    return emb.tolist()
