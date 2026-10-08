import logging
import uuid
from fastapi import FastAPI, Depends, HTTPException
from .auth import current_user
from .schemas import ChatRequest, ChatResponse
from .graph import graph
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
app=FastAPI(title="Walmart Claude Learning Lab")
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, user=Depends(current_user)):
    request_id=str(uuid.uuid4())
    logger.info("chat_started request_id=%s", request_id)
    try:
        result=await graph.ainvoke({"messages":[{"role":"user","content":body.message}],"permissions":user["permissions"],"answer":"","requested_tools":[]}, config={"recursion_limit":8})
    except Exception:
        logger.exception("chat_failed request_id=%s",request_id)
        raise HTTPException(503,"Assistant temporarily unavailable")
    logger.info("chat_finished request_id=%s",request_id)
    return ChatResponse(answer=result["answer"], conversation_id=body.conversation_id)
