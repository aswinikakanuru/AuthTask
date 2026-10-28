from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import User, CreateUser, Token, SessionDep
from services.register import register_user
from services.login import login_user
from services.token import get_current_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", summary="Register user")
def register(session: SessionDep, user_data: CreateUser):
    return register_user(session=session, user_data=user_data)


@router.post("/login", response_model=Token, summary="Login user")
def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_user(session=session, form_data=form_data)


@router.get("/profile", summary="Get protected user profile")
def profile(current_user: Annotated[User, Depends(get_current_user)]):
    return {"name": current_user.name, "email": current_user.email}