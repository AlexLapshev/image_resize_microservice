import asyncio

from celery import Celery
from pathlib import Path
from PIL import Image

from src.database.database import redis, ImageForResize
from src.logging_file import logger
from src.database.database import connect_to_db, disconnect_from_db


celery_app = Celery('image_resize', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

OUT_IMG_FOLDER = Path(__file__).parents[0].joinpath('imgs', 'resized')
OUT_IMG_FOLDER.mkdir(parents=True, exist_ok=True)


@celery_app.task(bind=True)
def resize_image_celery(self, image_path: str, height: int, width: int) -> None:
    task_id = self.request.id
    image_names = image_name_format(image_path)
    logger.info('OPENING IMAGE {}'.format(image_names.get('image_name_orig')))
    asyncio.get_event_loop().run_until_complete(update_image_in_redis(task_id, 'IN PROCESS', ''))
    image = Image.open(image_path)
    logger.info('RESIZING IMAGE task_id:{}, image_name: {}'.format(task_id, image_names.get('image_name_orig')))
    image = image.resize((height, width))
    image.save(OUT_IMG_FOLDER.joinpath(image_names.get('new_image_name')), optimize=True)
    out_path = str(OUT_IMG_FOLDER.joinpath(image_names.get('new_image_name')))
    asyncio.get_event_loop().run_until_complete(
        update_image_in_redis(task_id, 'SUCCESS', out_path)
    )
    logger.info('RESIZING COMPLETED task_id:{}, image_name: {}'.format(task_id, image_names.get('image_name_orig')))
    asyncio.get_event_loop().run_until_complete(save_to_db(task_id, out_path))
    logger.info('IMAGE SAVED to {}'.format(out_path))


def image_name_format(image_path: str) -> dict:
    image_full_name = str(Path(image_path).name)
    logger.info('CREATING IMAGE_NAME FROM {}'.format(image_full_name))
    image_name_orig = image_full_name.split('.')[0]
    image_extension = image_full_name.split('.')[-1]
    new_image_name = image_name_orig + '_resized.{}'.format(image_extension)
    logger.info('NEW IMAGE NAME {}'.format(new_image_name))
    return {'new_image_name': new_image_name, 'image_name_orig': image_name_orig}


async def update_image_in_redis(task_id: str, task_status: str, image_path='') -> None:
    await redis.hmset_dict(task_id, {'task_status': task_status, 'image_path': image_path})


async def save_to_db(image_task_id: str, image_path: str) -> None:
    await connect_to_db()
    img = await ImageForResize.create(image_task_id=image_task_id, image_path=image_path)
    logger.info('IMAGE ADDED TO DATABASE {}'.format(img.image_path))
    await disconnect_from_db()

