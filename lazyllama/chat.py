from queue import Queue
from threading import Thread

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown


class QueueCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue=None):
        self.queue = queue or Queue()

    def on_chat_model_start(self, *args, **kwargs):
        pass

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, *args, **kwargs):
        self.queue.put(None)


class StreamingChat:
    def __init__(self, message):
        self.message = message
        self.queue = Queue()

    def __iter__(self):
        Thread(target=self._generate).start()

        while True:
            if (token := self.queue.get()) is None:
                break
            else:
                yield token

    def _generate(self):
        ChatOpenAI(streaming=True)(
            messages=[HumanMessage(content=self.message)],
            callbacks=[QueueCallbackHandler(queue=self.queue)],
        )


def chat(message):
    tokens = ""
    with Live(console=Console(), refresh_per_second=10) as live:
        for token in StreamingChat(message):
            tokens += token
            live.update(Markdown(tokens))
