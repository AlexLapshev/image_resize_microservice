import asyncio
import os
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial

from PIL import Image

from aiohttp.web_request import FileField

from src.database import ImageForResize, Status
from src.logging_file import logger


OUT_IMG_FOLDER = os.path.join(os.path.dirname(__file__), 'imgs', 'resized')


async def image_to_db() -> int:
    img = await ImageForResize.create(image_status=1)
    logger.info('OPERATION ADDED TO DATABASE {}'.format(img.image_id))
    return img.image_id


def saving_image(img: Image, img_name: str, height: int, width: int) -> str:
    img = img.resize((height, width))
    img.save(OUT_IMG_FOLDER+img_name, optimize=True)
    logger.info('RESIZING COMPLETED')
    return 'finished'


async def resize_image(image: FileField, image_id: int, height: int, width: int) -> Image or None:
    logger.info('OPENING IMAGE')
    img_db = await ImageForResize.query.where(ImageForResize.image_id == image_id).gino.first()
    await img_db.update(image_status=2).apply()
    file_name = image.filename.split('.')[0]
    file_extension = image.filename.split('.')[-1]
    img = Image.open(image.file)
    logger.info('RESIZING IMAGE')
    img_name = '/' + file_name + '_resized{}.{}'.format(image_id, file_extension)
    thread_pool = ThreadPoolExecutor()
    loop = asyncio.get_running_loop()
    if res := await loop.run_in_executor(thread_pool, partial(saving_image, img, img_name, height, width)):
        await img_db.update(image_path=OUT_IMG_FOLDER + img_name, image_status=3).apply()


async def get_image_from_db(image_id: int):
    query = ImageForResize.outerjoin(Status).select()
    if image := await query.where(ImageForResize.image_id == image_id).gino.first():
        logger.info('GETTING IMAGE {} FROM DB'.format(image_id))
        return {'image_path': image.image_path, 'image_id': image.image_id, 'image_status': image.status_name}
    else:
        return
