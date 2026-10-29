from fastapi import HTTPException
from sqlmodel import select

from database import User, CreateUser, SessionDep
from services.token import hash_password


def register_user(session: SessionDep, user_data: CreateUser):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already Registered")

   
    hash_pwd = hash_password(user_data.password)

    user = User(email=user_data.email, name=user_data.name, hashed_password=hash_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user