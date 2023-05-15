from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown


class RichLiveMarkdownHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = ''
        self.live = Live(console=Console(), refresh_per_second=10)

    def on_chat_model_start(self, *args, **kwargs):
        self.live.start()

    def on_llm_start(self, *args, **kwargs):
        pass

    def on_llm_end(self, *args, **kwargs):
        self.live.stop()

    def on_llm_new_token(self, token, **kwargs):
        self.tokens += token
        self.live.update(Markdown(self.tokens))


def chat(message):
    ChatOpenAI(streaming=True)(
        messages=[HumanMessage(content=message)],
        callbacks=[RichLiveMarkdownHandler()],
    )
