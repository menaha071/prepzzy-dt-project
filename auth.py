from fastapi import APIRouter, HTTPException
from ..models.schemas import UserLogin, UserSignup
from ..services import auth_service

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/signup")
def signup(data: UserSignup):
    try:
        result = auth_service.signup(data.name, data.email, data.password)
        return {"success": True, "user": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(data: UserLogin):
    try:
        result = auth_service.login(data.email, data.password)
        return {"success": True, "user": result}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
