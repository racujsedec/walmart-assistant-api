from app.security.authorization import require_permission,can_view_order
from fastapi import HTTPException
async def get_shipment(order_id:str,principal:dict)->dict:
 require_permission(principal,'shipments:read')
 if not can_view_order(principal,order_id):raise HTTPException(403,'Not authorized')
 return {'order_id':order_id,'carrier':'Demo Carrier','tracking_status':'Delayed at sorting facility'}
