import aioredis
from src.settings import settings


from gino import Gino

db = Gino()
url = settings.postgres_url


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


async def connect_to_redis(app):
    redis_url = app["redis_url"]
    redis = await aioredis.create_redis_pool(redis_url, loop=app.loop)
    app["redis"] = redis


async def disconnect_from_redis(app):
    redis = app["redis"]
    redis.close()
    await redis.wait_closed()
