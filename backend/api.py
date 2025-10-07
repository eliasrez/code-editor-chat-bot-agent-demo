# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic",
#     "pydantic",
#     "fastapi",
#     "uvicorn",
#     "python-multipart",
# ]
# ///

import os
import sys
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
from main import AIAgent

app = FastAPI(title="AI Code Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and Create React App default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store agent instances per session (in production, use proper session management)
agents = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


class FileReadRequest(BaseModel):
    path: str


class FileListRequest(BaseModel):
    path: str = "."


def get_agent(session_id: str) -> AIAgent:
    """Get or create an agent for the given session"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not set")
    
    if session_id not in agents:
        agents[session_id] = AIAgent(api_key)
    
    return agents[session_id]


@app.get("/")
async def root():
    return {"message": "AI Code Assistant API is running"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Send a message to the AI agent"""
    try:
        agent = get_agent(request.session_id)
        response = agent.chat(request.message)
        return ChatResponse(response=response, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat response (for real-time updates)"""
    async def generate():
        try:
            agent = get_agent(request.session_id)
            response = agent.chat(request.message)
            
            # Send response in chunks for streaming effect
            words = response.split()
            for i, word in enumerate(words):
                chunk = word + (" " if i < len(words) - 1 else "")
                yield f"data: {json.dumps({'chunk': chunk, 'done': False})}\n\n"
                await asyncio.sleep(0.01)  # Small delay for smooth streaming
            
            yield f"data: {json.dumps({'chunk': '', 'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/files/read")
async def read_file(request: FileReadRequest):
    """Read a file's contents"""
    try:
        with open(request.path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"path": request.path, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {request.path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/files/list")
async def list_files(request: FileListRequest):
    """List files in a directory"""
    try:
        if not os.path.exists(request.path):
            raise HTTPException(status_code=404, detail=f"Path not found: {request.path}")
        
        items = []
        for item in sorted(os.listdir(request.path)):
            item_path = os.path.join(request.path, item)
            items.append({
                "name": item,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "path": item_path
            })
        
        return {"path": request.path, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/conversation/history/{session_id}")
async def get_conversation_history(session_id: str):
    """Get conversation history for a session"""
    if session_id not in agents:
        return {"messages": []}
    
    agent = agents[session_id]
    return {"messages": agent.messages}


@app.delete("/api/conversation/{session_id}")
async def clear_conversation(session_id: str):
    """Clear conversation history for a session"""
    if session_id in agents:
        del agents[session_id]
    return {"message": "Conversation cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
