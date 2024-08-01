from fastapi import FastAPI, HTTPException, Request, Depends, status, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from typing import Annotated
from datetime import datetime
from schemas.auth_schemas import SNewUser, SUser, SAuthUser, SAuth, SToken
from fastapi.security import OAuth2PasswordRequestForm
from interface.auth_interface import Auth_Interface
import logging
import asyncio

##################
import jwt
from datetime import datetime, timedelta
from config.auth_config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

logging.basicConfig(
    level=logging.DEBUG, 
    filename = "logs/auth.log", 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt='%H:%M:%S',
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


EXPIRATION_TIME = timedelta(minutes=30)

def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logging.info(f"sub: {payload.get("sub")} token: {token} ALGORITHM: {ALGORITHM}")
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        logging.info("ExpiredSignatureError")
        pass
    except jwt.InvalidTokenError:
        logging.info(f"InvalidTokenError token: {token}")
        pass
##################


auth_router = APIRouter(prefix="/api/auth")

@auth_router.post("/register")
async def register(data: SNewUser):
    if Auth_Interface.get_bool_user(data.name):
        await Auth_Interface.add_user(data)

@auth_router.post("/token", response_model=SToken)
async def login(user_data: OAuth2PasswordRequestForm = Depends()): # : SAuthUser
    data_db = await Auth_Interface.get_user(user_data.username)
    logging.info(f"call fun login")
    if data_db == None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
        )

    user_data_from_db = SUser.from_orm(data_db)
    if user_data.password != user_data_from_db.hash_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_jwt_token({"sub": user_data.username})}


