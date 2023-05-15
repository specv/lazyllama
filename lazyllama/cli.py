import typer

app = typer.Typer()


@app.command()
def chat(message: str):
    from .chat import chat

    chat(message)
