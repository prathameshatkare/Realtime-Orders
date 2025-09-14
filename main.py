import asyncio
import json
import aiomysql
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "realtime_demo")

connected_clients = set()
pool = None  # Global connection pool


async def notify_clients(message: dict):
    """Send message to all connected WebSocket clients."""
    disconnected = []
    for ws in connected_clients:
        try:
            await ws.send_text(json.dumps(message, default=str))
        except WebSocketDisconnect:
            disconnected.append(ws)
    for ws in disconnected:
        connected_clients.remove(ws)


async def watch_order_events():
    """Continuously watch order_events table for new rows and push to clients."""
    last_seen_id = 0
    global pool
    while True:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT id, payload, created_at FROM order_events WHERE id > %s ORDER BY id ASC",
                    (last_seen_id,),
                )
                rows = await cur.fetchall()
                for row in rows:
                    event_id, payload, created_at = row
                    last_seen_id = event_id
                    await notify_clients({"id": event_id, "payload": json.loads(payload), "created_at": str(created_at)})
        await asyncio.sleep(1)  # lightweight polling (not client polling)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    print("🔄 Connecting to database...")
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True,
    )
    print("✅ Database connected")

    # Start background watcher
    task = asyncio.create_task(watch_order_events())
    yield
    # Shutdown: cleanup
    task.cancel()
    await pool.wait_closed()
    print("🛑 Database connection closed")


app = FastAPI(lifespan=lifespan)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
@app.get("/")
async def home():
    return {"message": "Realtime Orders API is running 🚀"}