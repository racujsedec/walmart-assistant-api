from app.rag.keyword import lexical_score
# Local lexical reranker for a runnable demo; production uses a model-based reranker.
def rerank(query:str,chunks:list[dict])->list[dict]:
 return sorted(chunks,key=lambda c:lexical_score(query,c['text']),reverse=True)
