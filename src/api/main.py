from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from schemas.schemas import SItemAdd, SItemPrice, SPostRequest
from typing import Annotated
from datetime import datetime
from interface.redis_interface import Redis_Interface
from interface.interface import Interface
from interface.auth_interface import Auth_Interface
from auth_module.auth import oauth2_scheme, auth_router, get_user_from_token
from schemas.auth_schemas import SAuth, SToken
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    filename = "logs/api.log", 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt='%H:%M:%S',
)

@asynccontextmanager
async def lifespan(app: FastAPI):
   yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

@app.get("/api/data_item_{name}")
async def get_data_item(name: str):
   logging.info("The get_data_item function was called ")
   data = await Redis_Interface.find_item(name)
   return data

@app.get("/api/history_item_{name}")
async def get_history_item(name: str):
   logging.info("The get_history_item function was called ")
   data = await Interface.item_history(name)
   return data

@app.post("/api/search")
async def search(request_: SPostRequest):
   logging.info("The search function was called ")
   data = await Redis_Interface.find_items(request_.data, request_.category, request_.id)
   return data

@app.get("/api/user/")
async def get_user_info(current_user: str = Depends(get_user_from_token)): # SToken
   #current_user = get_user_from_token(token) #current_user = get_user_from_token(token.access_token)
   logging.info(f"current_user: {current_user}")
   data_db = await Auth_Interface.get_user(current_user)
   if data_db == None:
         raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid credentials",
               headers={"WWW-Authenticate": "Bearer"},
            )
   user_data = SAuth.from_orm(data_db)
   if user_data.role != "normal":
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
   return {"message": "Hello User!"}