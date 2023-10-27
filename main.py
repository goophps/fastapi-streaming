import asyncio
import os

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage, BaseMessage
from langchain.chat_models import ChatOpenAI
from starlette.responses import StreamingResponse

import request_model

# fastapi
app = FastAPI()

# openai
os.environ["OPENAI_API_KEY"] = 'your api key'


@app.post("/chat")
async def chat(req_model: request_model.Chat):
    callback = AsyncIteratorCallbackHandler()
    llm = ChatOpenAI(streaming=True, callbacks=[callback], temperature=0)
    messages = [HumanMessage(content=req_model.content)]
    return StreamingResponse(generate_stream_response(callback, llm, messages), media_type="text/event-stream")


async def generate_stream_response(_callback, llm: ChatOpenAI, messages: list[BaseMessage]):
    """流式响应"""
    task = asyncio.create_task(llm.apredict_messages(messages))
    async for token in _callback.aiter():
        yield token

    await task


# 跨域处理
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', port=8008, reload=True)
