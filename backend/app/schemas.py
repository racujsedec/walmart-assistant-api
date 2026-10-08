from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str = Field(min_length=1)
class ChatResponse(BaseModel):
    answer: str
    conversation_id: str
class OrderInput(BaseModel):
    order_id: str = Field(pattern=r"^[0-9]{1,30}$")
class OrderResult(BaseModel):
    order_id: str
    status: str
    estimated_delivery: str
