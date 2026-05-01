import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
from agent import TravelAgent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Travel Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = TravelAgent()

app.mount("/static", StaticFiles(directory="static"), name="static")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    response: str
    success: bool


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Convert history format for OpenAI-compatible chat APIs.
        history = []
        for msg in (request.history or []):
            role = msg.role if msg.role in ("user", "assistant", "system", "model") else "assistant"
            if role == "model":
                role = "assistant"
            history.append({"role": role, "content": msg.content})

        response = await agent.chat(request.message, history)
        return ChatResponse(response=response, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def legacy_chat(request: ChatRequest):
    result = await chat(request)
    return {"response": result.response}
