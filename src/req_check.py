from aiohttp import web
from aiohttp.web_request import Request, FileField
from pydantic import ValidationError
from pathlib import Path

from src.logging_file import logger
from src.errors_status import GetError
from src.check_req_pydantic import ImageUploadCheck


IN_IMG_FOLDER = Path(__file__).parents[0].joinpath('imgs', 'original')
IN_IMG_FOLDER.mkdir(parents=True, exist_ok=True)


async def check_request(request: Request) -> dict or None:
    data = await request.post()
    image = data.get('image')
    height = data.get('height')
    width = data.get('width')
    try:
        data = ImageUploadCheck(image=image, width=width, height=height)
        image = await save_original_image(data.image)
        checked_data = {'image_path': image, 'width': data.width, 'height': data.height}
        logger.info('SUCCESSFULLY CHECKED')
        return checked_data
    except ValidationError as e:
        return e.errors()[0]


async def save_original_image(image: FileField) -> str:
    full_path = IN_IMG_FOLDER.joinpath(image.filename)
    with open(full_path, 'wb+') as file_path:
        for chunk in image.file:
            file_path.write(chunk)
    return str(full_path)


async def check_id_field(request: Request) -> web.json_response or dict:
    if image_id := request.rel_url.query.get('id'):
        logger.info('CHECKING ID: {}'.format(image_id))
        redis = request.app['redis']
        image = await redis.hmget(image_id, 'task_status', encoding='utf-8')
        if image[0]:
            logger.info('IMAGE FOUND: {}'.format(image_id))
            return {
                'image_id': image_id,
                'transaction_status': image[0]
            }
        else:
            logger.info('NO IMAGE WITH ID {}'.format(image_id))
            return GetError('no task found', 404, str(image_id)).create_response_error()
    logger.warning('INCORRECT FIELD NAME')
    return GetError('incorrect field name', 400).create_response_error()
