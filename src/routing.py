from aiohttp import web
from aiohttp.web_request import Request

from src.database.database import ImageForResize
from src.req_check import check_id_field, check_request
from src.errors_status import PostError, GetError
from src.tasks import resize_image_celery

routes = web.RouteTableDef()


@routes.post("/api/v1/send_picture")
async def send_picture(request: Request) -> web.json_response:
    if int(request.headers['Content-Length']) > 11**7:
        return web.json_response(PostError('image', 'image is too big', 400))
    data = await check_request(request)
    if data.get('msg'):
        return PostError(data.get('loc')[0], data.get('msg'), 400).create_response_error()
    redis = request.app['redis']
    task = resize_image_celery.delay(image_path=data.get('image_path'),
                                     height=data.get('height'), width=data.get('width'))
    await redis.hmset_dict(task.id, {'task_status': task.status, 'image_path': ''})
    return web.json_response({'task_id': task.id, 'task_status': task.status})


@routes.get("/api/v1/get_transaction_status")
async def get_status(request: Request) -> web.json_response:
    image = await check_id_field(request)
    if type(image) == dict:
        return web.json_response({"image_id": image.get('image_id'),
                                  "transaction_status": image.get('transaction_status')}, status=200)
    return image


@routes.get("/api/v1/get_resized")
async def get_resized_image(request: Request) -> web.FileResponse or web.json_response:
    if image_id := request.rel_url.query.get('id'):
        if image := await ImageForResize.query.where(ImageForResize.image_task_id == image_id).gino.first():
            return web.FileResponse(image.image_path, status=200)
        else:
            return GetError('Image not found', 404, image_id).create_response_error()
    else:
        return GetError('No field id', 400,).create_response_error()


