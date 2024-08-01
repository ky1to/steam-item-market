from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from config.auth_config import AUTH_POSTGRES_USER, AUTH_POSTGRES_PASSWORD, AUTH_POSTGRES_DB
import datetime

engine = create_async_engine(
    f"postgresql+asyncpg://{AUTH_POSTGRES_USER}:{AUTH_POSTGRES_PASSWORD}@postgres_user_db:5432/{AUTH_POSTGRES_DB}"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class UserTable(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    hash_password: Mapped[str]
    role: Mapped[str]

class FavoritesTable(Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    name_item: Mapped[str]

class InventoryTable(Model):
    __tablename__ = 'inventory'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    name_item: Mapped[str]
    price: Mapped[float]
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

#async def create_table():
#    async with engine.begin() as conn:
#        await conn.run_sync(Model.metadata.create_all)

#async def delete_table():
#    async with engine.begin() as conn:
#        await conn.run_sync(Model.metadata.drop_all)