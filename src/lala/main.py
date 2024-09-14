from litestar import Litestar, post, Request
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import RedocRenderPlugin
from pydantic import BaseModel
from lala.llamacpp import model


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
