from datetime import datetime, timedelta
from typing import Dict, List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# ======================
# Configuration
# ======================

SECRET_KEY = "replace-with-secure-secret"
ALGORITHM = "HS256"

security = HTTPBearer()

# ======================
# In-memory data store
# ======================

receipts_db: List[Dict] = [
    {"id": 1, "tenant_id": "tenant_a", "amount": 50.0},
    {"id": 2, "tenant_id": "tenant_a", "amount": 20.0},
    {"id": 3, "tenant_id": "tenant_b", "amount": 100.0},
]

# ======================
# JWT helpers
# ======================

def decode_token(token: str) -> Dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

# ======================
# Auth dependency
# ======================

def get_identity(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict:
    """
    Single source of truth:
    tenant_id is trusted ONLY if it comes from JWT payload.
    """
    payload = decode_token(credentials.credentials)

    # Enforce required JWT fields
    for field in ("sub", "tenant_id", "role"):
        if field not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Missing required JWT field: {field}",
            )

    return {
        "user_id": payload["sub"],
        "tenant_id": payload["tenant_id"],
        "role": payload["role"],
    }

# ======================
# FastAPI app
# ======================

app = FastAPI(title="Code Audit Slice: JWT Tenant Isolation")

@app.get("/receipts")
def get_receipts(identity: Dict = Depends(get_identity)):
    """
    Multi-tenant isolation is enforced here.
    tenant_id is sourced ONLY from JWT payload.
    """
    tenant_id = identity["tenant_id"]

    return [
        r for r in receipts_db
        if r["tenant_id"] == tenant_id
    ]
