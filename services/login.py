from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from database import User, SessionDep
from services.token import verify_password, create_access_token


def login_user(session: SessionDep, form_data: OAuth2PasswordRequestForm):
    user = session.exec(select(User).where(User.email == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

   
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}