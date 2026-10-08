import json,os,re
from pathlib import Path
PROMPTS=Path(__file__).resolve().parents[1]/'prompts'
SYSTEM=(PROMPTS/'system.md').read_text()
TOOLS=[{'name':'get_order_status','description':'Read current order status','input_schema':{'type':'object','properties':{'order_id':{'type':'string'}},'required':['order_id']}},
 {'name':'get_shipment','description':'Read shipment tracking','input_schema':{'type':'object','properties':{'order_id':{'type':'string'}},'required':['order_id']}},
 {'name':'get_inventory','description':'Read inventory for order','input_schema':{'type':'object','properties':{'order_id':{'type':'string'}},'required':['order_id']}},
 {'name':'search_return_policy','description':'Find approved return policy evidence','input_schema':{'type':'object','properties':{'query':{'type':'string'}},'required':['query']}}]
async def ask_claude(messages:list[dict],allowed_tools:list[str]|None=None)->dict:
 allowed_tools=allowed_tools or [t['name'] for t in TOOLS]
 if os.getenv('LLM_MODE','mock')=='mock':
  last=messages[-1]
  if last['role']=='user' and isinstance(last['content'],str):
   q=last['content'];m=re.search(r'\b\d{5,20}\b',q);order_id=m.group(0) if m else '12345'
   names=['get_order_status','get_shipment','get_inventory','search_return_policy']
   return {'text':'','tool_calls':[{'id':f'demo-{i}','name':name,'input':{'query':q} if name=='search_return_policy' else {'order_id':order_id}} for i,name in enumerate(names) if name in allowed_tools]}
  results=[]
  for msg in messages:
   if isinstance(msg.get('content'),list):
    for block in msg['content']:
     if block.get('type')=='tool_result':results.append(f"{block['tool_use_id']}: {block['content']}")
  return {'text':'Verified demo evidence: '+ ' | '.join(results)[:1400],'tool_calls':[]}
 if os.getenv('LLM_MODE')!='anthropic':raise RuntimeError('LLM_MODE must be mock or anthropic')
 from anthropic import AsyncAnthropic
 if not os.getenv('ANTHROPIC_API_KEY'):raise RuntimeError('ANTHROPIC_API_KEY missing')
 client=AsyncAnthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
 response=await client.messages.create(model=os.getenv('CLAUDE_MODEL','claude-sonnet-4-5'),max_tokens=900,system=SYSTEM,messages=messages,tools=[t for t in TOOLS if t['name'] in allowed_tools])
 return {'text':' '.join(b.text for b in response.content if b.type=='text'), 'tool_calls':[{'id':b.id,'name':b.name,'input':b.input} for b in response.content if b.type=='tool_use'], 'raw_blocks':[b.model_dump() for b in response.content]}
