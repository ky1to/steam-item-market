from fastapi import FastAPI, Request, Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from schemas.schemas import SItemAdd, SItemPrice, SPostRequest
from typing import Annotated
from interface.interface import Interface
from datetime import datetime
from interface.redis_interface import Redis_Interface

@asynccontextmanager
async def lifespan(app: FastAPI):
   yield

app = FastAPI(lifespan=lifespan)

@app.get("/api/data_item_{name}")
async def get_data_item(name: str):
   data = await Redis_Interface.find_item(name)
   return data

@app.get("/api/history_item_{name}")
async def get_data_item(name: str):
   data = await Interface.item_history(name)
   return data

@app.post("/api/search")
async def get_data_item(request_: SPostRequest):
   data = await Redis_Interface.find_items(request_.data, request_.category, request_.id)
   return data