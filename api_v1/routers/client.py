from fastapi import APIRouter, Depends, Request, HTTPException
import httpx
from starlette import status

from api_v1.depends.client import get_message_content
from models.message import Message
from schemas.message import MessageSchema
from utils.config import config

router = APIRouter(prefix="/client", tags=["client"])


@router.post("/send_message", response_model=MessageSchema)
async def send_message(
    request: Request, message: MessageSchema = Depends(get_message_content)
):
    message = await Message.create(
        Message(
            title=message.title,
            content=message.content,
            contact=message.contact,
            client_id=message.client_id,
            client_msg_ip=request.client.host,
        )
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"https://api.telegram.org/bot{config.APP_TG_BOT_TOKEN}/sendMessage",
            data={
                "chat_id": config.APP_TG_CHAT_ID,
                "text": f"{message.content}\n"
                f"\n"
                f"From: {message.title}\n"
                f"Contact: {message.contact}",
            },
        )
        if response.status_code == httpx.codes.OK:
            return {"status": "ok"}

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal Server Error",
    )
