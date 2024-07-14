from threading import Thread
from typing import Any

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler

from queue import Queue

from dotenv import load_dotenv
from langchain_core.outputs import LLMResult

load_dotenv()


chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([("human", "{content}")])

# messages = prompt.format_messages(content="tell me a joke")

# for message in chat.stream(messages):
#     print(message)


# chain은 기본적으로 stream 기능을 제공하지 않음
# chain = LLMChain(llm=chat, prompt=prompt)

# for output in chain.stream(input={"content": "tell me a joke"}):
#     print(output)


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


class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            self(input, callbacks=[handler])

        Thread(target=task).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token


class StreamingChain(StreamableChain, LLMChain):
    pass


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)
