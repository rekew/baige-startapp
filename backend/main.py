from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.modules.admin.api import admin
from app.modules.user.api import auth, user
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("🚀 Application startup")
    yield
    print("🛑 Application shutdown")
    await engine.dispose()


app = FastAPI(title="Baige App", version="0.0.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9999",
        "http://127.0.0.1:9999",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to the Baige App API!"}