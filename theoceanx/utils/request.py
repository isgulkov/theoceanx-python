import aiohttp

class Request:
    async def request(self, url):
        async with aiohttp.ClientSession() as session:
            params = [('key', 'value1'), ('key', 'value2')]
            async with session.get('https://api.github.com/events', params=params) as resp:
                print(resp.status)
                print(await resp.text())