from app.llm.claude_client import ask_claude
async def call_claude(state:dict)->dict:
 response=await ask_claude(state['messages'])
 calls=response.get('tool_calls',[])
 if calls:
  # Anthropic requires an assistant tool_use message before the matching user tool_result.
  blocks=response.get('raw_blocks') or [{'type':'tool_use','id':c['id'],'name':c['name'],'input':c['input']} for c in calls]
  return {'requested_tools':calls,'messages':state['messages']+[{'role':'assistant','content':blocks}]}
 return {'answer':response.get('text',''),'requested_tools':[]}
