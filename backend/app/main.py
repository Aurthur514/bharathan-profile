from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import create_db_and_tables
from .api import router
from .engine import start_engine, stop_engine
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting SentinelSight...")
    create_db_and_tables()
    task = start_engine()
    yield
    # Shutdown logic
    print("Shutting down SentinelSight...")
    stop_engine()
    await task

app = FastAPI(title="SentinelSight API", lifespan=lifespan)
app.include_router(router)

# Mount snapshots for serving
if not os.path.exists("snapshots"):
    os.makedirs("snapshots")
app.mount("/snapshots", StaticFiles(directory="snapshots"), name="snapshots")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
