from app.security.authorization import require_permission,can_view_order
from fastapi import HTTPException
async def get_inventory(order_id:str,principal:dict)->dict:
 require_permission(principal,'inventory:read')
 if not can_view_order(principal,order_id):raise HTTPException(403,'Not authorized')
 return {'order_id':order_id,'availability':'Replacement stock available in demo warehouse'}
