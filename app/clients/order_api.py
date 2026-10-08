import os,httpx
async def fetch_order(order_id:str)->dict:
 async with httpx.AsyncClient(timeout=5) as client:
  r=await client.get(f"{os.getenv('ORDER_API_URL','http://127.0.0.1:8001')}/orders/{order_id}")
  r.raise_for_status();return r.json()
