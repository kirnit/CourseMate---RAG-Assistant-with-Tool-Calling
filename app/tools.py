def make_search_documents(rag_pipeline):
    def search_documents(query):
        return rag_pipeline.search(query, top_k=3)

    return search_documents


search_documents_schema = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Ищет информацию в университетских PDF-документах. "
            "Возвращает релевантные фрагменты с названием документа "
            "и номером страницы.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Поисковый запрос по загруженному PDF"
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}