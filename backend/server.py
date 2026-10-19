import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import run_pipeline
from core.rag_engine import ask_question

app = FastAPI(title="AI Video Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# session_id -> rag_chain (kept in memory, lost when the server restarts)
SESSIONS: dict = {}


class ProcessRequest(BaseModel):
    source: str
    language: str = "english"


class ChatRequest(BaseModel):
    session_id: str
    question: str


def _text(value) -> str:
    """Make sure whatever the pipeline returns is a plain string for the UI."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "content"):  # LangChain message objects
        return str(value.content)
    return str(value)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Plain `def` (not async) so FastAPI runs these blocking calls in a thread pool
# and the server stays responsive while Whisper / LLM calls are running.
@app.post("/api/process")
def process(req: ProcessRequest):
    if not req.source.strip():
        raise HTTPException(status_code=400, detail="Source is required")

    try:
        result = run_pipeline(source=req.source.strip(), language=req.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = result["rag_chain"]

    return {
        "session_id": session_id,
        "title": _text(result["title"]),
        "summary": _text(result["summary"]),
        "action_items": _text(result["action_items"]),
        "key_decisions": _text(result["key_decisions"]),
        "open_questions": _text(result["open_questions"]),
        "transcript": _text(result["transcript"]),
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    rag_chain = SESSIONS.get(req.session_id)
    if rag_chain is None:
        raise HTTPException(
            status_code=404,
            detail="Session expired. Please analyze the video again.",
        )

    try:
        answer = ask_question(rag_chain, req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {e}")

    return {"answer": _text(answer)}