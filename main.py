from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
import uvicorn

from database import engine
from routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="AuthTask",
    description="FastAPI Authentication with PostgreSQL, SQLModel, and JWT",
    version="1.0.0",
    lifespan=lifespan,
)

# Connect router
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "project": "AuthTask",
        "database": "PostgreSQL",
        "message": "API is online! Go to /docs for Swagger UI",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)