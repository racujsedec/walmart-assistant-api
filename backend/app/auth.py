import os
from fastapi import Header, HTTPException

def current_user(authorization: str | None = Header(default=None)):
    # Local demo only. In production validate OIDC JWT signature, issuer, audience and expiry.
    if authorization != "Bearer " + os.getenv("DEMO_AUTH_TOKEN", "local-associate-token"):
        raise HTTPException(401, "Invalid associate token")
    return {"id": "associate-782", "permissions": ["orders:read"]}
