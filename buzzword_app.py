import asyncio
from aiohttp import web

from buzzword_indexer import BuzzwordIndexer
from hn_client import HackerNewsClient


async def index(request):
    return web.FileResponse('static/index.html')


async def get_buzzword(request):
    indexer = request.app['buzzword_indexer']
    response = web.WebSocketResponse()
    is_socket_available = response.can_prepare(request)
    if not is_socket_available:
        return web.json_response(indexer.state)

    await response.prepare(request)
    await response.send_json(indexer.state)

    request.app['websockets'].append(response)
    try:
        async for message in response:
            pass
    finally:
        request.app['websockets'].remove(response)
    return response


async def monitor_hn(app):
    indexer = app['buzzword_indexer']
    client = app['hn_client']
    while True:
        max_item = await client.get_max_item()
        if indexer.max_item and max_item > indexer.max_item:
            for i in range(indexer.max_item + 1, max_item + 1, ):
                item = await client.get_item(i)
                indexer.process_item(item)
        await asyncio.sleep(5)


async def crawl_hn(app):
    indexer = app['buzzword_indexer']
    client = app['hn_client']
    start_item = indexer.min_item or await client.get_max_item()
    for i in range(start_item, 0, -1):
        item = await client.get_item(i)
        indexer.process_item(item)


async def broadcast_state(app):
    indexer = app['buzzword_indexer']
    while True:
        state = indexer.state
        for ws in app['websockets']:
            try:
                await ws.send_json(state)
            except:
                app['websockets'].remove(ws)
        await asyncio.sleep(5)


async def persist_indexer(app):
    indexer = app['buzzword_indexer']
    while True:
        indexer.persist()
        await asyncio.sleep(5)


async def on_shutdown(app):
    app['hn_crawler'].cancel()
    app['hn_monitor'].cancel()
    app['broadcast_state'].cancel()
    app['persist_indexer'].cancel()
    app['hn_client'].close()
    for ws in app['websockets']:
        await ws.close()


async def start_background_tasks(app):
    app['hn_crawler'] = app.loop.create_task(crawl_hn(app))
    app['hn_monitor'] = app.loop.create_task(monitor_hn(app))
    app['broadcast_state'] = app.loop.create_task(broadcast_state(app))
    app['persist_indexer'] = app.loop.create_task(persist_indexer(app))


def init_app():
    app = web.Application()
    app['websockets'] = []
    app['buzzword_indexer'] = BuzzwordIndexer()
    app['buzzword_indexer'].load()
    app['hn_client'] = HackerNewsClient()
    app.add_routes([web.get('/', index),
                    web.get('/api/v1/buzzword/', get_buzzword),
                    web.static('/static', 'static', append_version=True)])

    app.on_shutdown.append(on_shutdown)
    app.on_startup.append(start_background_tasks)

    return app
