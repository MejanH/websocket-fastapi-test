from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware


app =  FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
     data = await websocket.receive_text()
     print("Message received from client: " + data)
     await websocket.send_text(f"Yo!, what's up? You sent me: {data}")