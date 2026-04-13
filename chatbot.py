from fastapi import APIRouter
from ..models.schemas import ChatRequest
from ..services.chatbot_service import get_response

router = APIRouter(prefix="/api", tags=["chatbot"])


@router.post("/chat")
def chat(data: ChatRequest):
    response = get_response(data.message)
    return {"success": True, "response": response}
