from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Nexus Enterprise Twin...")
    yield
    print("Shutting down Nexus Enterprise Twin...")


app = FastAPI(
    title="Nexus Enterprise Twin",
    description="AI Operating System for Organizational Intelligence",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["System"], summary="Platform Status")
def root():
    return {
        "platform": "Nexus Enterprise Twin",
        "version": "0.1.0",
        "status": "running"
    }
