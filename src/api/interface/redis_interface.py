from interface.interface import Interface
from schemas.schemas import SItem
import redis.asyncio as redis
import json

redis_host = "redis"
redis_port = "6379"

class Redis_Interface:
    @classmethod
    async def find_item(cls, data: str):
        async with redis.Redis(host=redis_host, port=redis_port, db=0) as redis_client:
            request_data = await redis_client.keys(f"{data}")
            if request_data != []:
                request = await redis_client.lindex(request_data[0], 0)
                return json.loads(request)
            item_db = await Interface.name_get_item(data)
            await redis_client.lpush(item_db.name, item_db.id, json.dumps(item_db.dict()))
            await redis_client.expire(item_db.name, 60)
            return item_db

    @classmethod 
    async def find_items(cls, data: str, category: str, id: int):
        if category == "None":
            category = None
        return_data = []
        async with redis.Redis(host=redis_host, port=redis_port, db=0) as redis_client:
            request_data = await redis_client.keys(f"*{data}*")
            if request_data != []:
                for i in range((id-1)*10+1, id*10, 1):
                    for item_redis in request_data:
                        if int(await redis_client.lindex(item_redis, -1)) == i:
                            request_data_f = await redis_client.lindex(item_redis, 0)
                            if category != "":
                                if json.loads(request_data_f)["disc"] == category:
                                    return_data.append(json.loads(request_data_f))
                            else:
                                return_data.append(json.loads(request_data_f))
                if return_data != [] and len(return_data) > 9:
                    return return_data
            request_data_db = await Interface.find_item(data, category, id)
            for item_db in request_data_db:
                await redis_client.lpush(item_db.name, item_db.id, json.dumps(item_db.dict()))
                await redis_client.expire(item_db.name, 60)
            return request_data_db