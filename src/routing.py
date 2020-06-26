import asyncio

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from src.img_transform import resize_image, image_to_db
from src.req_check import check_id_field, check_request
from src.errors_status import PostError

routes = web.RouteTableDef()


@routes.post("/api/v1/send_picture")
async def send_picture(request: Request) -> web.json_response:
    if int(request.headers['Content-Length']) > 11**7:
        return web.json_response({"error": "image size is too big"})
    data = await check_request(request)
    if type(data) == dict:
        return PostError(data.get('loc')[0], data.get('msg'), 400).create_response_error()
    else:
        image, height, width = data
        image_id = await image_to_db()
        asyncio.create_task(resize_image(image, image_id, height, width))
        return web.json_response({"transaction_status": "CREATED", "image_id": image_id}, status=201)


@routes.get("/api/v1/get_transaction_status/")
async def get_status(request: Request) -> web.json_response:
    image = await check_id_field(request)
    if type(image) == dict:
        return web.json_response({"transaction_status": image.get('image_status'),
                                  "image_id": image.get('image_id')}, status=200)
    else:
        return image


@routes.get("/api/v1/get_resized")
async def get_resized_image(request: Request) -> web.FileResponse or json_response:
    image = await check_id_field(request)
    if type(image) == dict:
        return web.FileResponse(image.get('image_path'))
    else:
        return image
