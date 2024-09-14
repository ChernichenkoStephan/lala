from pydantic import Field, BaseModel
from llama_cpp import Llama
from os import environ as env


class LlamaCppRuntimeConfig(BaseModel):
    path: str = Field(alias="LLAMA_MODEL_PATH")
    n_ctx: int = Field(alias="LLAMA_MODEL_N_CTX")
    top_k: int = Field(alias="LLAMA_MODEL_TOP_K")
    top_p: float = Field(alias="LLAMA_MODEL_TOP_P")
    temperature: float = Field(alias="LLAMA_MODEL_TEMPERATURE")
    repeat_penalty: float = Field(alias="LLAMA_MODEL_REPEAT_PENALTY")
    verbose: bool = Field(alias="LLAMA_MODEL_VERBOSE")
    n_gpu_layers: int = Field(alias="LLAMA_MODEL_N_GPU_LAYERS")


class LlamaCppRuntime:
    def __init__(
        self,
        config: LlamaCppRuntimeConfig,
    ):
        self._model = Llama(
            model_path=config.path,
            n_ctx=config.n_ctx,
            n_parts=1,
            response_format="json_object",
            verbose=config.verbose,
            n_gpu_layers=config.n_gpu_layers,
        )
        self._top_k = config.top_k
        self._top_p = config.top_p
        self._temperature = config.temperature
        self._repeat_penalty = config.repeat_penalty
        self._model_name = config.path.split("/")[-1]

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        res = self._model.create_chat_completion(
            [
                {"role": "user", "content": user_prompt},
                {"role": "system", "content": system_prompt},
            ],
            temperature=self._temperature,
            top_k=self._top_k,
            top_p=self._top_p,
            repeat_penalty=self._repeat_penalty,
        )
        match res:
            case {"choices": [{"message": {"content": str(content)}}]}:
                return content
            case _:
                raise ValueError(f"Expected dict, got {type(res)}")

    async def __call__(self, system_prompt: str, user_prompt: str) -> str:
        return self.complete(system_prompt, user_prompt)


conf = LlamaCppRuntimeConfig(**env)
model = LlamaCppRuntime(conf)
