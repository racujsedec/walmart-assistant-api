# A real refund must call a separately authenticated Returns Service.
# Local demo records an approval only; no money is moved.
async def submit_refund(order_id:str,amount:float,idempotency_key:str)->dict:
 return {'refund_id':f'demo-refund-{order_id}','status':'APPROVED_DEMO_ONLY'}
