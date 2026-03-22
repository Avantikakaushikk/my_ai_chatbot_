from fastapi import APIRouter
from models.chat_model import ChatRequest
from services.llm_service import get_response
from database import get_history, save_message

router = APIRouter(prefix="/chat")

@router.post("/")
async def chat(req: ChatRequest):
    user_id = req.user_id
    message = req.message

    # Save user message to database
    save_message(user_id, "user", message)

    # Fetch history
    history = get_history(user_id)

    # Get response from OpenAI using the full history context
    response = await get_response(history)

    # Save assistant response to database
    save_message(user_id, "assistant", response)

    return {"response": response}