from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "nexus-demo-secret-change-later"
ALGORITHM = "HS256"

DEMO_USERS = {
    "ceo@nexus.com": {"password": "ceo123", "role": "CEO", "name": "Chief Executive Officer"},
    "coo@nexus.com": {"password": "coo123", "role": "COO", "name": "Chief Operating Officer"},
    "manager@nexus.com": {"password": "manager123", "role": "MANAGER", "name": "Operations Manager"},
    "employee@nexus.com": {"password": "employee123", "role": "EMPLOYEE", "name": "Employee"},
}


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=8)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(email: str, password: str):
    user = DEMO_USERS.get(email)

    if not user or user["password"] != password:
        return None

    token = create_token({
        "email": email,
        "role": user["role"],
        "name": user["name"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": email,
            "role": user["role"],
            "name": user["name"]
        }
    }
