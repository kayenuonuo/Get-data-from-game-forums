from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from agent import agent_executor   # ← 直接 import 你写好的 AgentExecutor

app = FastAPI()


# ========== 1. 请求体模型 ==========
class ChatRequest(BaseModel):
    message: str


# ========== 2. 首页，返回 HTML ==========
@app.get("/")
async def index():
    return FileResponse(path="./index.html")


# ========== 3. 聊天接口，调用你的 Agent ==========
@app.post("/chat")
async def chat(req: ChatRequest):
    result = await agent_executor.ainvoke({"input": req.message})
    return {"data": result["output"]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)