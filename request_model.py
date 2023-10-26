import re
from pydantic import BaseModel, Field


class Chat(BaseModel):
    content: str = Field(description='发送信息',max_length=1000)
    temperature: float = Field(default=0, description='温度(值越小，聊天机器人的回答越精简；反之，回答则富有创造力)', ge=0,le=1)
