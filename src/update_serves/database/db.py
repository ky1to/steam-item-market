from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from config.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
import datetime

engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres_db:5432/{POSTGRES_DB}"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass
 
class SteamTable(Model):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    game: Mapped[str]
    item_nameid: Mapped[int]
    link: Mapped[str]
    img_link: Mapped[str]
    disc: Mapped[str | None]

class ItemPrice(Model):
    __tablename__ = 'prices'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    price_buy: Mapped[float]
    price_sell: Mapped[float]
    price_profit: Mapped[float]
    sell_lots: Mapped[int]
    buy_lots: Mapped[int]


#async def create_table():
#    async with engine.begin() as conn:
#        await conn.run_sync(Model.metadata.create_all)

#async def delete_table():
#    async with engine.begin() as conn:
#        await conn.run_sync(Model.metadata.drop_all)