import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def post(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:8080'
        data = {'move': '1'} # this is JSON
        # Check that we have connected to the server and have comms 
        html = await fetch(session, url)
        print(html)
        # Send a post to the server with fake move data
        html = await post(session, url, data)
        print(html)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())