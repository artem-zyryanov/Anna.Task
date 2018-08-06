from aiohttp import ClientSession


class HackerNewsClient:
    URL_PREFIX = 'https://hacker-news.firebaseio.com/v0'

    def __init__(self):
        # Атата
        self.client = ClientSession()

    def close(self):
        self.client.close()

    async def get_max_item(self):
        return await self._get_resource(f'{self.URL_PREFIX}/maxitem.json')

    async def get_item(self, id):
        return await self._get_resource(f'{self.URL_PREFIX}/item/{id}.json')

    async def _get_resource(self, uri):
        async with self.client.get(uri) as resp:
            return await resp.json()