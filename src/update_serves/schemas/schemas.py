from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SPostRequest(BaseModel):
    data: str
    category: str
    id: int

class SItemAdd(BaseModel):
    name: str
    game: str
    item_nameid: int
    link: str
    img_link: str
    disc: Optional[str] = None
    model_config = ConfigDict(strict=True, from_attributes=True)

class SItem(SItemAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SItemPrice(BaseModel):
    name: str
    timestamp: datetime
    price_buy: float
    price_sell: float
    price_profit: float
    sell_lots: int
    buy_lots: int
    model_config = ConfigDict(strict=True, from_attributes=True)
