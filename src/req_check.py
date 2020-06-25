from aiohttp.web_request import Request

from src.logging_file import logger
from src.errors_status import Errors
from src.img_transform import get_image_from_db


APPROVED_EXTENSIONS = ['png', 'jpeg', 'jpg']


async def check_request(request: Request) -> list or None:
    data = await request.post()
    image = data.get('image')
    height = data.get('height')
    width = data.get('width')
    checked_data = []
    if image:
        logger.info('CHECKING IMAGE')
        file_extension = image.filename.split('.')[-1]
        if file_extension in APPROVED_EXTENSIONS:
            checked_data.append(image)
    if height.isdigit() and int(height) < 10000:
        checked_data.append(int(height))
    if width.isdigit() and int(width) < 10000:
        checked_data.append(int(width))
    if len(checked_data) == 3:
        logger.info('SUCCESSFULLY CHECKED')
        return checked_data
    else:
        logger.info('INCORRECT DATA')
        return


async def check_id_field(request: Request):
    if image_id := request.rel_url.query.get('id'):
        logger.info('CHECKING ID: {}'.format(image_id))
        if image_id.isdigit():
            image_id = int(image_id)
        else:
            return Errors.web_response(400)
        if image := await get_image_from_db(image_id):
            logger.info('IMAGE FOUND: {}'.format(image_id))
            return image
        else:
            logger.info('NO IMAGE WITH ID {}'.format(image_id))
            return Errors.web_response(404)
    logger.info('INCORRECT FIELD NAME')
    return Errors.web_response(400)
