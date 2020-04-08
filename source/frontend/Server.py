
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def post_handle(request):
    text = await request.text()
    print(text)
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.post('/', post_handle),
                web.post('/{name}', post_handle)])

if __name__ == '__main__':
    web.run_app(app)