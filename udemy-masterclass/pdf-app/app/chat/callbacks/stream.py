from typing import Any
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue) -> None:
        self.queue = queue

    # OpenAI에서 텍스트 청크를 스트리밍해주면 아래 함수가 호출됨
    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        self.queue.put(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        self.queue.put(None)

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> Any:
        self.queue.put(None)
