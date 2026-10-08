import os,re,uuid,json,asyncio
from fastapi import APIRouter,Depends,Header,HTTPException
from fastapi.responses import StreamingResponse
from app.security.jwt import current_user
from app.schemas.chat import ChatRequest,ChatResponse
from app.agents.graph import graph
from app.approvals.service import propose_refund,confirm_refund
router=APIRouter()
async def process(body:ChatRequest,principal:dict)->dict:
 state=await graph.ainvoke({'messages':[{'role':'user','content':body.message}],'principal':principal,'requested_tools':[],'tool_results':[],'citations':[]},config={'recursion_limit':8})
 approval=None
 if re.search(r'\brefund\b',body.message,re.I):
  order=re.search(r'\b\d{5,20}\b',body.message)
  if order and not any('error' in r.get('result',{}) for r in state.get('tool_results',[]) if r['name']=='get_order_status'):
   # This is a demo proposal, not a verified production eligibility decision.
   approval=propose_refund(order.group(0),principal)
 return ChatResponse(conversation_id=body.conversation_id,answer=state.get('answer','No answer'),citations=state.get('citations',[]),approval=approval,trace_id=str(uuid.uuid4())).model_dump()
@router.post('/chat',response_model=ChatResponse)
async def chat(body:ChatRequest,principal:dict=Depends(current_user)):return await process(body,principal)
@router.post('/chat/stream')
async def chat_stream(body:ChatRequest,principal:dict=Depends(current_user)):
 async def generate():
  yield 'event: progress\ndata: '+json.dumps({'message':'Checking order, shipment, inventory and policy…'})+'\n\n'
  try:
   result=await process(body,principal)
   yield 'event: final\ndata: '+json.dumps(result)+'\n\n'
  except Exception:
   yield 'event: error\ndata: '+json.dumps({'message':'Unable to complete the request; check backend logs'})+'\n\n'
 return StreamingResponse(generate(),media_type='text/event-stream',headers={'Cache-Control':'no-cache','X-Accel-Buffering':'no'})
@router.post('/approvals/{approval_id}/confirm')
async def confirm(approval_id:str,decision:dict,principal:dict=Depends(current_user),idempotency_key:str|None=Header(None)):
 if decision.get('decision')!='approve':raise HTTPException(400,'Unsupported decision')
 return confirm_refund(approval_id,principal,idempotency_key or '')
