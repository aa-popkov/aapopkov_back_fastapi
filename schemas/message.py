from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=2000)
    contact: str = Field(min_length=3, max_length=255)
    client_id: int
