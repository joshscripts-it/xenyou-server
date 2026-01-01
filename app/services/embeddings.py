from sentence_transformers import SentenceTransformer

# import numpy as np
# import faiss


# class EmbeddingService:
#     def __init__(self):
#         self.model = SentenceTransformer("all-MiniLM-L6-v2")
#         self.index = None
#         self.items = []

#     def build_index(self, items):
#         self.items = items
#         embs = np.array([self.model.encode(i["description"]) for i in items]).astype(
#             "float32"
#         )
#         faiss.normalize_L2(embs)
#         self.index = faiss.IndexFlatIP(embs.shape[1])
#         self.index.add(embs)

#     def search(self, query, k=5):
#         q_emb = self.model.encode(query).astype("float32").reshape(1, -1)
#         faiss.normalize_L2(q_emb)
#         D, I = self.index.search(q_emb, k)
#         return [self.items[i] for i in I[0]]


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text: str):
        return self.model.encode(text).tolist()
