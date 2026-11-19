def chunk_pages(pages, chunk_size=500, overlap=100):
    chunks = []

    if chunk_size <= 0: raise ValueError("chunk_size должен быть положительным")
    if not 0 <= overlap < chunk_size: raise ValueError("overlap должен быть от 0 до chunk_size - 1")

    chunk_step = chunk_size - overlap
    
    for page in pages:
        text = page["text"]
        for start in range(0, len(text), chunk_step):

            frame = text[start:start+chunk_size]

            chunks.append(
                {
                    "document": page["document"],
                    "page": page["page"],
                    "chunk_id": len(chunks),
                    "text": frame
                }
            )
            
            if start+chunk_size >= len(text):
                break

    return chunks