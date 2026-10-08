from pydantic import BaseModel,Field
class ChatRequest(BaseModel):
 message:str=Field(min_length=1,max_length=4000)
 conversation_id:str=Field(min_length=1,max_length=128)
class Citation(BaseModel):
 id:str;title:str;source:str;excerpt:str
class ApprovalOut(BaseModel):
 id:str;order_id:str;amount:float;currency:str;status:str
class ChatResponse(BaseModel):
 conversation_id:str;answer:str;citations:list[Citation]=[];approval:ApprovalOut|None=None;trace_id:str
