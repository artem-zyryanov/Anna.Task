from aiohttp import web
from buzzword_app import init_app

web.run_app(init_app())
