from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import auth, user

app = FastAPI(title="Baige App", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9999",
        "http://127.0.0.1:9999"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(user.router, prefix="/api", tags=["Users"])


@app.get("/")
def root():
    return {"message": "Welcome to the Baige App API!"}
