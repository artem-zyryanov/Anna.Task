from aiohttp import web


async def index(request):
    return web.FileResponse('static/index.html')


app = web.Application()
app['websockets'] = []

app.add_routes([web.get('/', index),
                web.static('/static', 'static', append_version=True)])

web.run_app(app)
