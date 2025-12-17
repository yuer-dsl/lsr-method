from datetime import timedelta
from fastapi.testclient import TestClient
from jose import jwt
import pytest

from main import app, SECRET_KEY, ALGORITHM

client = TestClient(app)

# ======================
# Test helpers
# ======================

def make_token(payload: dict) -> str:
    data = payload.copy()
    data["exp"] = 9999999999
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# ======================
# Tests
# ======================

def test_tenant_a_can_only_see_its_own_data():
    token = make_token({
        "sub": "user_1",
        "tenant_id": "tenant_a",
        "role": "user",
    })

    res = client.get(
        "/receipts",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert all(r["tenant_id"] == "tenant_a" for r in data)


def test_query_param_cannot_override_tenant():
    token = make_token({
        "sub": "user_2",
        "tenant_id": "tenant_a",
        "role": "user",
    })

    res = client.get(
        "/receipts?tenant_id=tenant_b",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert all(r["tenant_id"] == "tenant_a" for r in data)


def test_missing_role_rejected():
    token = make_token({
        "sub": "user_3",
        "tenant_id": "tenant_a",
        # role missing
    })

    res = client.get(
        "/receipts",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 401
