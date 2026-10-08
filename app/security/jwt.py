import os
from fastapi import Header,HTTPException
async def current_user(authorization:str|None=Header(None)):
 # Fail closed outside the local demo. Real deployment needs OIDC/JWKS signature, iss/aud/exp verification.
 if os.getenv('DEMO_MODE','false').lower()=='true' and authorization=='Bearer local-associate-token':
  return {'id':'associate-demo','permissions':['orders:read','shipments:read','inventory:read','policies:read','refunds:approve'],'store':'DEMO'}
 raise HTTPException(401,'Demo token not accepted; configure real OIDC before production')
