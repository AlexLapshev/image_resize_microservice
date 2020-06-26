from aiohttp.web_request import Request
from pydantic import ValidationError

from src.logging_file import logger
from src.errors_status import GetError
from src.img_transform import get_image_from_db
from src.check_req_pydantic import ImageUploadCheck


async def check_request(request: Request) -> list or None:
    data = await request.post()
    image = data.get('image')
    height = data.get('height')
    width = data.get('width')
    try:
        data = ImageUploadCheck(image=image, width=width, height=height)
        checked_data = [data.image, data.width, data.height]
        logger.info('SUCCESSFULLY CHECKED')
        return checked_data
    except ValidationError as e:
        return e.errors()[0]


async def check_id_field(request: Request):
    if image_id := request.rel_url.query.get('id'):
        logger.info('CHECKING ID: {}'.format(image_id))
        if image_id.isdigit():
            image_id = int(image_id)
        else:
            return GetError('incorrect id number: {}'.format(image_id), 400).create_response_error()
        if image := await get_image_from_db(image_id):
            logger.info('IMAGE FOUND: {}'.format(image_id))
            return image
        else:
            logger.info('NO IMAGE WITH ID {}'.format(image_id))
            return GetError('no image found', 404, str(image_id)).create_response_error()
    logger.info('INCORRECT FIELD NAME')
    return GetError('incorrect field name', 400).create_response_error()
