from database.db import new_session, SteamTable, ItemPrice
from schemas.schemas import SItemAdd, SItemPrice, SItem
from sqlalchemy import select

class Interface:
    @classmethod
    async def add_one(cls, data: SItemAdd):
        async with new_session() as session:
            data_dict = data.model_dump()
            line = SteamTable(**data_dict)
            session.add(line)
            await session.commit()
            return line.id

    @classmethod 
    async def add_one_history(cls, data: SItemPrice):
        async with new_session() as session:
            data_dict = data.model_dump()
            line = ItemPrice(**data_dict)
            session.add(line)
            await session.commit()
            return line.id
    
    @classmethod 
    async def find_all(cls):
        async with new_session() as session:
            query = select(SteamTable)
            result = await session.execute(query)
            model = result.scalars().all()
            return model

    @classmethod 
    async def name_get_item(cls, name_f: str):
        async with new_session() as session:
            query = select(SteamTable).filter_by(name=name_f)
            result = await session.execute(query)
            model = result.scalars().all()
            return SItem.from_orm(model[0])

    @classmethod 
    async def item_history(cls, name_f: str):
        async with new_session() as session:
            query = select(ItemPrice).filter_by(name=name_f)
            result = await session.execute(query)
            model = result.scalars().all()
            return model

    @classmethod 
    async def find_item(cls, data: str, category: str, id: int):
        async with new_session() as session:
            if category == "":
                query = select(SteamTable).where(SteamTable.name.ilike(f'%{data}%'))
            else:
                if category == "None":
                    category = None
                query = select(SteamTable).filter_by(disc=category).where(SteamTable.name.ilike(f'%{data}%'))
            result = await session.execute(query)
            model = result.scalars().all()
            len_arr = len(model)
            aut_arr = []
            for i in range((id-1)*10, id*10, 1):
                if i < len_arr:
                    aut_arr.append(SItem.from_orm(model[i]))
            return aut_arr