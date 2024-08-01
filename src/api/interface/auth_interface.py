from database.user_db import new_session, UserTable
from schemas.auth_schemas import SUser, SNewUser
from sqlalchemy import select

class Auth_Interface:
    @classmethod
    async def get_user(cls, name: str):
        async with new_session() as session:
            query = select(UserTable).where(UserTable.name.ilike(name))
            result = await session.execute(query)
            model = result.scalars().all()
            if model == []:
                return None
            return model[0]

    @classmethod
    async def add_user(cls, data: SNewUser):
        async with new_session() as session:
            data_dict = data.model_dump()
            data_dict['role'] = 'normal'
            line = UserTable(**data_dict)
            session.add(line)
            await session.commit()
    
    @classmethod
    async def get_bool_user(cls, name: str):
        async with new_session() as session:
            query = select(UserTable).where(UserTable.name.ilike(name))
            result = await session.execute(query)
            model = result.scalars()
            if model:
                return True
            else:
                return False 