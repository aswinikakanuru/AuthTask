from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from database import User, SessionDep
from services.token import verify_password, create_access_token


def login_user(session: SessionDep, form_data: OAuth2PasswordRequestForm):
    # 1. Look up user by email in PostgreSQL
    user = session.exec(select(User).where(User.email == form_data.username)).first()

    # 2. Validate password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    # 3. Generate JWT token
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}