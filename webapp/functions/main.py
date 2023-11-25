# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

import json
import re

from firebase_functions import https_fn
from firebase_admin import initialize_app
initialize_app()

from flask import Flask, jsonify, request
app = Flask(__name__)
app.json.ensure_ascii = False

from google.cloud import aiplatform
from langchain.chat_models import ChatVertexAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
chatVertexAI = ChatVertexAI(temperature=0.3, max_output_tokens=2048)

@app.get("/example")
def on_request_example():
    res = chatVertexAI([
        SystemMessage(content="あなたは何を食べるべきかを提案する AI アシスタントです"),
        HumanMessage(content="私はトマトが好きです。何を食べるべきですか？")
    ])
    content = res.content
    print(content)
    return Flask.Response(status=200, response=content)



# curl 例 
# curl -X POST -H "Content-Type: application/json" -d '{"content":"私はトマトが好きです。何を食べるべきですか？"}' http://127.0.0.1:5001/vertex-ai-chat-agent/us-central1/httpsflaskexample/api/chat
@app.post("/api/chat")
def chat():    
    data = request.json
    print(data)
    res = chatVertexAI([
        SystemMessage(content="あなたはおすすめレシピを要約して提案する AIアシスタント です。説明などをつけないシンプルな json形式 で回答してください。英語で作成したあと日本語に翻訳してください。"),
        HumanMessage(content=data.get("content"))
    ])
    print( res.content )
    result = {"content": ""}
    # マークダウン形式で json が返ってくるので、それを整形する
    json_match = re.search(r'```json\n([\s\S]*?)\n```', res.content)
    if json_match:
        result = json.loads( json_match.group(1) )
    print( result )
    return jsonify(result)

@https_fn.on_request()
def httpsflaskexample(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
