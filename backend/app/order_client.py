import os
import httpx
async def fetch_order(order_id: str):
    url = os.getenv("ORDER_API_URL", "http://localhost:8001").rstrip("/") + f"/orders/{order_id}"
    headers = {"Authorization": "Bearer " + os.getenv("ORDER_API_TOKEN", "local-demo-token")}
    async with httpx.AsyncClient(timeout=3.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
