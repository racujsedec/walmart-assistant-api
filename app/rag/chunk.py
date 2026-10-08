def chunk_text(text:str,size:int=450,overlap:int=60)->list[str]:
 if not (size>overlap>=0):raise ValueError('size must exceed overlap')
 chunks=[];start=0
 while start<len(text):
  end=min(start+size,len(text));chunks.append(text[start:end]);
  if end==len(text):break
  start=end-overlap
 return chunks
