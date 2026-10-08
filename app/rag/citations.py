def citations_from_chunks(chunks:list[dict])->list[dict]:
 return [{'id':c['id'],'title':c['title'],'source':c['source'],'excerpt':c['text'][:260]} for c in chunks]
