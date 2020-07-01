from pydantic import BaseModel, validator
from aiohttp.web_request import FileField

from src.logging_file import logger

APPROVED_EXTENSIONS = ['png', 'jpeg', 'jpg']


class ImageUploadCheck(BaseModel):
    image: FileField
    width: str
    height: str

    @validator('image')
    def image_check(cls, v):
        logger.info('CHECKING IMAGE {}'.format(v.filename))
        file_extension = v.filename.split('.')[-1]
        if file_extension in APPROVED_EXTENSIONS:
            return v
        else:
            raise ValueError('Image extension is wrong: {}'.format(file_extension))

    @validator('width')
    def width_check(cls, v):
        logger.info('CHECKING WIDTH: {}'.format(v))
        if v.isdigit() and int(v) < 10001:
            return int(v)
        logger.warning('INCORRECT WIDTH: {}'.format(v))
        raise ValueError('Width is incorrect: {}'.format(v))

    @validator('height')
    def check_height(cls, v):
        logger.info('CHECKING HEIGHT: {}'.format(v))
        if v.isdigit() and int(v) < 10001:
            return int(v)
        logger.warning('INCORRECT HEIGHT: {}'.format(v))
        raise ValueError('Height is incorrect: {}'.format(v))

    class Config:
        arbitrary_types_allowed = True
