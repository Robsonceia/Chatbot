from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
import aioredis

app = FastAPI()


redis = aioredis.from_url("redis-10133.c60.us-west-1-2.ec2.redns.redis-cloud.com:10133")


websocket_connections = {}


client_id_counter = 0

@app.websocket("Robson-free-db/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    websocket_connections[client_id] = websocket
    pubsub = redis.pubsub()
    await pubsub.subscribe("chat")
    try:
        while True:
            message = await websocket.receive_text()
            await redis.publish("chat", f"Client {client_id}: {message}")
            await broadcast(pubsub)
    finally:
        del websocket_connections[client_id]
        await pubsub.unsubscribe("chat")

async def broadcast(pubsub):
    async for message in pubsub.listen():
        if message['type'] == 'message':
            for connection in websocket_connections.values():
                await connection.send_text(message['data'].decode('utf-8'))

@app.get("/")
async def get():
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

app.mount("/static", StaticFiles(directory="static"), name="static")
