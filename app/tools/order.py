from app.schemas.tools import OrderInput,OrderResult
from app.clients.order_api import fetch_order
from app.security.authorization import require_permission,can_view_order
from fastapi import HTTPException
async def get_order_status(order_id:str,principal:dict)->dict:
 order_id=OrderInput(order_id=order_id).order_id
 require_permission(principal,'orders:read')
 if not can_view_order(principal,order_id):raise HTTPException(403,'Order not in demo entitlement')
 raw=await fetch_order(order_id)
 return OrderResult(order_id=raw['order_id'],status=raw['status'],estimated_delivery=raw.get('estimated_delivery')).model_dump()
