"""
Simple auth service with in-memory storage.
Replace with Supabase integration for production.
"""

import hashlib
import uuid

_users = {}
_sessions = {}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def signup(name: str, email: str, password: str) -> dict:
    if email in _users:
        raise ValueError("Email already registered")
    
    user_id = str(uuid.uuid4())
    _users[email] = {
        "id": user_id,
        "name": name,
        "email": email,
        "password_hash": hash_password(password),
    }
    
    token = str(uuid.uuid4())
    _sessions[token] = user_id
    
    return {"id": user_id, "name": name, "email": email, "token": token}


def login(email: str, password: str) -> dict:
    user = _users.get(email)
    if not user or user["password_hash"] != hash_password(password):
        raise ValueError("Invalid credentials")
    
    token = str(uuid.uuid4())
    _sessions[token] = user["id"]
    
    return {"id": user["id"], "name": user["name"], "email": user["email"], "token": token}


from typing import Optional

def get_user(token: str) -> Optional[dict]:
    user_id = _sessions.get(token)
    if not user_id:
        return None
    for email, user in _users.items():
        if user["id"] == user_id:
            return {"id": user["id"], "name": user["name"], "email": user["email"]}
    return None
