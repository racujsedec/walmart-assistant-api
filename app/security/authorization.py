from fastapi import HTTPException
def require_permission(principal:dict,permission:str):
 if permission not in principal.get('permissions',[]):raise HTTPException(403,f'Missing permission: {permission}')
def can_view_order(principal:dict,order_id:str)->bool:
 # Replace with resource-level entitlements in the real Order Service.
 return principal.get('store')=='DEMO' and order_id=='12345'
