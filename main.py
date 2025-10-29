from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["whiteboard_db"]

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("app/static/index.html") as f:
        return HTMLResponse(f.read())

@app.get("/get-canvas")
async def get_canvas():
    canvas = await db.canvas.find_one({"_id": "current"})
    return canvas or {}

@app.post("/save-canvas")
async def save_canvas(data: dict):
    await db.canvas.update_one({"_id": "current"}, {"$set": data}, upsert=True)
    return {"message": "Canvas saved!"}

