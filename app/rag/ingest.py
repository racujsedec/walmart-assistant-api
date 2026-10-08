from pathlib import Path
from app.rag.chunk import chunk_text
POLICY=Path(__file__).resolve().parents[2]/'data'/'policies'/'DEMO_RETURN_POLICY.txt'
def local_chunks():
 return [{'id':f'policy-{i}','title':'Demo delayed-order policy','source':str(POLICY),'text':t,'approved':True,'market':'DEMO'} for i,t in enumerate(chunk_text(POLICY.read_text()))]
