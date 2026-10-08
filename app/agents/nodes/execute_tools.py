import json,asyncio
from app.tools.order import get_order_status
from app.tools.shipment import get_shipment
from app.tools.inventory import get_inventory
from app.tools.policy import search_return_policy
TOOLS={'get_order_status':get_order_status,'get_shipment':get_shipment,'get_inventory':get_inventory,'search_return_policy':search_return_policy}
async def execute_tools(state:dict)->dict:
 principal=state['principal'];calls=state.get('requested_tools',[])
 async def run(c):
  try:
   name=c['name'];args=c['input']
   if name not in TOOLS:raise ValueError('Tool not allowlisted')
   result=await TOOLS[name](**args,principal=principal)
   return {'name':name,'result':result,'id':c['id']}
  except Exception as exc:return {'name':c['name'],'result':{'error':type(exc).__name__,'detail':str(exc)[:200]},'id':c['id']}
 results=await asyncio.gather(*(run(c) for c in calls))
 blocks=[{'type':'tool_result','tool_use_id':r['id'],'content':json.dumps(r['result'],default=str)} for r in results]
 citations=[c for r in results if r['name']=='search_return_policy' for c in r['result'].get('citations',[])]
 return {'messages':state['messages']+[{'role':'user','content':blocks}],'requested_tools':[],'tool_results':results,'citations':citations}
