import os
from typing import Optional, Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session

# 1. Load DATABASE_URL from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("CRITICAL ERROR: DATABASE_URL is not set in the .env file!")

# 2. Pure PostgreSQL Engine
engine = create_engine(DATABASE_URL, echo=True)


# 3. User Table in PostgreSQL
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str


class CreateUser(SQLModel):
    name: str
    email: str
    password: str


class LoginUser(SQLModel):
    email: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


# 4. Dependency function to yield a PostgreSQL session
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]