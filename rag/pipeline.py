from rag.pdf_loader import load_pdf
from rag.chunker import chunk_pages
from rag.embeddings import EmbeddingModel
from rag.retriever import Retriever
from rag.generator import LLMGenerator

class RAGPipeline:
    def __init__(self, pdf_path):
        self.pages = load_pdf(pdf_path)
        self.chunks = chunk_pages(self.pages)
        self.embedding_model = EmbeddingModel()
        self.retriever = Retriever(self.chunks, self.embedding_model)
        self.generator = None

    def search(self, query, top_k=3):
        return self.retriever.search(query, top_k=top_k)

    def build_context(self, results):
        context = []
        for i in range(len(results)):
            context.append(
                f"[Источник {i+1}]\n"
                f"Документ: {results[i]['document']}\n"
                f"Страница: {results[i]['page']}\n"
                f"Текст: {results[i]['text']}\n")
        return "\n\n".join(context)

    def get_unique_sources(self, results):
        seen = set()
        unique_res = []
        for dic in results:
            info = (dic["document"], dic["page"])
            if info not in seen:
                seen.add(info)
                unique_res.append(dic)
        return unique_res


    def ask(self, question):
        context = self.search(question)
        if not context: return {
                                "answer": "Недостаточно данных для ответа",
                                "sources": []
                            }
        prompt = self.build_context(context)
        if self.generator is None: self.generator = LLMGenerator()
        response = self.generator.generate(question, prompt)

        info = {}
        info["answer"] = response
        info["sources"] = self.get_unique_sources([{"document": res["document"], "page": res["page"]} for res in context])
        return info