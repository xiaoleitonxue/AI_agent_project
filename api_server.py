from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.react_agent import ReactAgent
import uvicorn
from typing import Optional

app = FastAPI(title="智扫通智能客服API", version="1.0")

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

agent_instances = {}

def get_or_create_agent(session_id: str) -> ReactAgent:
    if session_id not in agent_instances:
        agent_instances[session_id] = ReactAgent()
    return agent_instances[session_id]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id or "default"
        agent = get_or_create_agent(session_id)

        response_chunks = []
        for chunk in agent.execute_stream(request.message):
            response_chunks.append(chunk)

        full_response = "".join(response_chunks).strip()

        return ChatResponse(
            response=full_response,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
