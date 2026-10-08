from .schemas import OrderInput, OrderResult
from .order_client import fetch_order
async def get_order_status(order_id: str, permissions: list[str]) -> dict:
    if "orders:read" not in permissions:
        return {"error": "FORBIDDEN"}
    parsed = OrderInput(order_id=order_id)
    raw = await fetch_order(parsed.order_id)
    # Allow-list: only these three fields reach Claude; never return raw API JSON.
    return OrderResult(order_id=raw["order_id"], status=raw["status"], estimated_delivery=raw["estimated_delivery"]).model_dump()
