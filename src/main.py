from aiohttp import web


from src.routing import routes
from src.database.database import connect_to_db, disconnect_from_db

app = web.Application(client_max_size=10**8)
app.on_startup.append(connect_to_db)
app.on_shutdown.append(disconnect_from_db)
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)


