from aiohttp import web
from src.routing import routes
from src.database.database import connect_to_redis, disconnect_from_redis, connect_to_db, disconnect_from_db
from src.settings import settings


def create_app() -> web.Application:
    app = web.Application(client_max_size=10 ** 8)
    app["redis_url"] = settings.redis_url
    app.on_startup.append(connect_to_redis)
    app.on_startup.append(connect_to_db)
    app.on_shutdown.append(disconnect_from_redis)
    app.on_shutdown.append(disconnect_from_db)
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)
