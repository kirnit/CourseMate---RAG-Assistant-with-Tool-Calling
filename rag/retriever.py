import numpy as np

class Retriever:
    def __init__(self, chunks, embedding_model):
        self.chunks = chunks
        self.embedding_model = embedding_model

        self.embeddings = self.embedding_model.encode_chunks(chunks)

    def search(self, query, top_k=3):
        if not self.chunks:
            return []
        
        if top_k <= 0: raise ValueError("Некорректное значение top_k")
        embedded_query = self.embedding_model.encode_query(query)

        scores = self.embeddings @ embedded_query
        top_indices = np.argsort(scores)[::-1][:top_k]
        result = []
        for ind in top_indices:
            result.append(self.chunks[ind].copy())
            result[-1]["score"] = float(scores[ind])
        return result

