from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.app.api.routes import user, auth
from backend.app.db.session import engine


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

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(user.router, prefix="/api", tags=["Users"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Baige App API!"}