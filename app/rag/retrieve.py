from app.rag.ingest import local_chunks
from app.rag.keyword import lexical_score
from app.rag.rerank import rerank
from app.rag.fusion import reciprocal_rank_fusion
from app.rag.citations import citations_from_chunks
def search_policy(query:str)->list[dict]:
 chunks=local_chunks();lex=sorted(chunks,key=lambda c:lexical_score(query,c['text']),reverse=True)
 # Demo uses two lexical variations to demonstrate fusion. It is NOT semantic/vector retrieval.
 ids=reciprocal_rank_fusion([[c['id'] for c in lex],[c['id'] for c in chunks]])
 selected=rerank(query,[next(c for c in chunks if c['id']==id_) for id_ in ids])[:3]
 return citations_from_chunks(selected)
