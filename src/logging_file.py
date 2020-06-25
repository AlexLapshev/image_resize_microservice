import logging

logger = logging.getLogger('IMG_RESIZE')
logger.setLevel(logging.INFO)
logging.getLogger('gino').setLevel(logging.WARNING)
logging.getLogger('aiohttp').setLevel(logging.WARNING)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s:%(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)
