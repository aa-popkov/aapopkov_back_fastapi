from datetime import datetime, timedelta

from fastapi import Header, HTTPException, Form, Depends
from starlette import status
from starlette.requests import Request

from models.client import Client
from models.message import Message
from schemas.message import MessageSchema


async def get_client(
    request: Request,
    x_token: str | None = Header(),
):
    if x_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate request",
        )
    client_ip = request.client.host
    client = await Client.get_by_token_id(x_token)
    if not client:
        client = await Client.create(
            Client(frontend_id=x_token, client_last_ip=client_ip)
        )
    else:
        await Client.update_ip(x_token, client_ip)

    return client


async def get_last_client_date(client: Client = Depends(get_client)):
    last_date = await Message.get_last_date_client_msg(client.id)
    if last_date:
        cur_date = datetime.utcnow()
        date_diff = (cur_date - last_date).total_seconds()
        if date_diff < 3600:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't send messages more than 1 time per hour!"
            )
    return client


def get_message_content(
    title: str = Form(min_length=3, max_length=255),
    contact: str = Form(min_length=5, max_length=255),
    content: str = Form(max_length=2000),
    client: Client = Depends(get_last_client_date),
):
    if not title or not content or not contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Empty form"
        )
    return MessageSchema(
        title=title, content=content, client_id=client.id, contact=contact
    )
