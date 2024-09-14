from vllm import LLM, SamplingParams
from pydantic import Field, BaseModel
from os import environ as env


class VllmRuntimeConfig(BaseModel):
    path: str = Field(alias="LLAMA_MODEL_PATH")
    n_ctx: int = Field(alias="LLAMA_MODEL_N_CTX")
    top_k: int = Field(alias="LLAMA_MODEL_TOP_K")
    top_p: float = Field(alias="LLAMA_MODEL_TOP_P")
    temperature: float = Field(alias="LLAMA_MODEL_TEMPERATURE")
    repeat_penalty: float = Field(alias="LLAMA_MODEL_REPEAT_PENALTY")
    verbose: bool = Field(alias="LLAMA_MODEL_VERBOSE")
    n_gpu_layers: int = Field(alias="LLAMA_MODEL_N_GPU_LAYERS")


class VllmRuntime:
    def __init__(
        self,
        config: VllmRuntimeConfig,
    ):
        self._model = LLM(model=config.path)
        self._model_name = config.path.split("/")[-1]

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        sampling_params = SamplingParams(
            temperature=0.5, top_p=0.95, top_k=40, repetition_penalty=1.1
        )
        res = self._model.chat(
            [
                {"role": "user", "content": user_prompt},
                {"role": "system", "content": system_prompt},
            ],
            sampling_params=sampling_params,
        )
        match res:
            case {"choices": [{"message": {"content": str(content)}}]}:
                return content
            case _:
                raise ValueError(f"Expected dict, got {type(res)}")

    async def __call__(self, system_prompt: str, user_prompt: str) -> str:
        return self.complete(system_prompt, user_prompt)


conf = VllmRuntimeConfig(**env)
model = VllmRuntime(conf)
