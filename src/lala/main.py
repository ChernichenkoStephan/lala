from litestar import Litestar, post, Request
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import RedocRenderPlugin
from pydantic import BaseModel
import os
from typing import Protocol


class Model(Protocol):
    async def __call__(self, system_prompt: str, user_prompt: str) -> str: ...


model: Model

runtime = os.environ.get("LLM_RUNTIME", "llama_cpp")
if runtime == "llama_cpp":
    from lala.llamacpp import model as llama_cpp_model

    model = llama_cpp_model
elif runtime == "vllm":
    from lala.vllms import model as vllm_model

    model = vllm_model
else:
    raise ValueError(f"Invalid runtime: {runtime}")


class ChatRequest(BaseModel):
    system_prompt: str
    user_prompt: str


class ChatResponse(BaseModel):
    response: str


@post("/chat")
async def chat(request: Request, data: ChatRequest) -> ChatResponse:
    request.logger.info("Received chat request")
    return ChatResponse(response=await model(data.system_prompt, data.user_prompt))


app = Litestar(
    [chat],
    openapi_config=OpenAPIConfig(
        title="Lala",
        description="Lala",
        version="0.0.1",
        render_plugins=[RedocRenderPlugin()],
        path="/docs",
    ),
)
