# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import initialize_app
initialize_app()

from google.cloud import aiplatform
from langchain.chat_models import ChatVertexAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
chat = ChatVertexAI()

@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    res = chat([
        SystemMessage(content="あなたは何を食べるべきかを提案する AI アシスタントです"),
        HumanMessage(content="私はトマトが好きです。何を食べるべきですか？")
    ])
    content = res.content
    print(content)    
    return https_fn.Response(content)
