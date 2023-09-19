import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import openai

# Load .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def stream_openai_response_chunks(response):
    for chunk in response:
        current_content = chunk["choices"][0]["delta"].get("content", "")
        yield current_content


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    openai_api_key = os.getenv("OPEN_AI_API_KEY")
    # Assume some code here to set up your OpenAI API usage with the obtained API key

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        try:
            parsed_data = json.loads(data)
            prompt = parsed_data.get("prompt", "No prompt key found")
            print(f"Message received from client: {prompt}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                stream=True,
                messages=[{"role": "user", "content": prompt}],
            )
            for message_chunk in stream_openai_response_chunks(response):
                await websocket.send_text(message_chunk)
        except json.JSONDecodeError:
            await websocket.send_text("Invalid JSON format received.")
