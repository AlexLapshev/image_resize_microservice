import asyncio
from gino import Gino
import aioredis

db = Gino()
url = 'postgresql://db_user:123456@db/image_microservice'


class ImageForResize(db.Model):
    __tablename__ = 'images'

    image_id = db.Column(db.Integer(), primary_key=True)
    image_task_id = db.Column(db.String())
    image_path = db.Column(db.String())


async def connect_to_db(*args, **kwargs):
    await db.set_bind(url)
    # await db.gino.create_all()


async def disconnect_from_db(*args, **kwargs):
    await db.pop_bind().close()


async def connect_to_redis(*args, **kwargs):
    redis = await aioredis.create_redis_pool('redis://redis/0')
    return redis

redis = asyncio.get_event_loop().run_until_complete(connect_to_redis())
