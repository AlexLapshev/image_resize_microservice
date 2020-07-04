# Simple image resize app

## Installation

pip3 install -r requirements.txt

### Run

To run app you should set _settings_ variable in `settings.py`.

_DevConfig_ - `python -m src.main` to run app locally, with local _Postgres_, _Celery_, _Redis_ running.

_ProdConfig_ - `docker-compose up` in _/src_ to run app.

_TestsConfig_ - `docker-compose up` in _/src/tests/_ to run tests.

## Requires

python => 3.8

aiohttp

aioredis

gino

celery

Pillow

pydantic

redis

pytest

pytest-aiohttp
