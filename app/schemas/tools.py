from pydantic import BaseModel,Field
class OrderInput(BaseModel):order_id:str=Field(pattern=r'^\d{1,20}$')
class OrderResult(BaseModel):order_id:str;status:str;estimated_delivery:str|None=None
class ShipmentResult(BaseModel):order_id:str;carrier:str;tracking_status:str
class InventoryResult(BaseModel):order_id:str;availability:str
