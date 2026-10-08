from app.rag.retrieve import search_policy
from app.security.authorization import require_permission
async def search_return_policy(query:str,principal:dict)->dict:
 require_permission(principal,'policies:read')
 return {'citations':search_policy(query)}
