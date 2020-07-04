import pytest
from redis import Redis
import pathlib

from aiohttp import FormData
from aiohttp.test_utils import TestClient

from src.main import create_app
from src.settings import settings


@pytest.fixture(autouse=True)
def insert_in_redis() -> None:
    redis = Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_database)
    redis.hmset('af90a559-14c2-4fd2-ad10-d1573b5195e0', {'task_status': 'SUCCESS', 'image_path': 'image_path'})
    yield
    redis.flushall()


@pytest.fixture
def app(loop, aiohttp_client) -> TestClient:
    return loop.run_until_complete(aiohttp_client(create_app()))


@pytest.mark.parametrize('image_id, status', [({'id': 'af90a559-14c2-4fd2-ad10-d1573b5195e0'}, 200),
                                              ({'id': 'incorrect id'}, 404),
                                              ({'incorrect_field_name': 2}, 400),
                                              ({}, 400)
                                              ])
async def test_get_transaction_status(app: TestClient, image_id: dict, status: int):
    resp = await app.get('/api/v1/get_transaction_status', params=image_id)
    assert resp.status == status


@pytest.mark.parametrize('image_id, status', [({'id': 'af90a559-14c2-4fd2-ad10-d1573b5195e0'}, 200),
                                              ({'id': 'incorrect id'}, 404),
                                              ({'incorrect_field_name': 2}, 400),
                                              ({}, 400)
                                              ])
async def test_get_resized(app: TestClient, image_id: dict, status: int) -> None:
    print(type(app))
    resp = await app.get('/api/v1/get_resized', params=image_id)
    assert resp.status == status


@pytest.mark.parametrize('test_data, status', [(('test.jpg', '100', '100'), 200),
                                               (('test.jpg', '', '100'), 400),
                                               (('test.jpg', '100', ''), 400),
                                               (('test.test', '100', '100'), 400),
                                               (('test.jpg', '10001', '100'), 400),
                                               (('test.jpg', '100', '10001'), 400)])
async def test_send_image_data(app: TestClient, test_data: tuple, status: int) -> None:
    image_path = pathlib.Path(__file__).parent.absolute().joinpath('data_test', test_data[0])
    data = FormData()
    data.add_field('image', open(image_path, 'rb'), filename=test_data[0])
    data.add_field('height', test_data[1])
    data.add_field('width', test_data[2])
    resp = await app.post('/api/v1/send_picture', data=data)
    assert resp.status == status


@pytest.mark.parametrize('test_data, status', [(('image', 'test.jpg', 'height', '100'), 400),
                                               (('image', 'test.jpg', 'width', '100'), 400),
                                               (('height', '100', 'width', '100'), 400)
                                               ])
async def test_send_image_no_field(app: TestClient, test_data: tuple, status: int) -> None:
    data = FormData()
    try:
        image_path = pathlib.Path(__file__).parent.absolute().joinpath('data_test', test_data[1])
        data.add_field('image', open(image_path, 'rb'), filename=test_data[1])
    except FileNotFoundError as e:
        data.add_field(test_data[0], test_data[1])
    data.add_field(test_data[2], test_data[3])
    resp = await app.post('/api/v1/send_picture', data=data)
    assert resp.status == status
