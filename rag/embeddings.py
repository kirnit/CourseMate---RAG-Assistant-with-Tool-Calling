from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def encode_chunks(self, chunks):
        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,
                convert_to_numpy=True
            )

        return embeddings

    def encode_query(self, query):
        return self.model.encode_query(query, normalize_embeddings=True, convert_to_numpy=True)