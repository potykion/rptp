from sanic import Sanic
from sanic import response

from rptp.getters import video_getter

app = Sanic()


@app.route('/api/videos')
async def video_api_view(request):
    query = request.args.get('query')
    token = request.headers.get('authorization')

    videos = await video_getter(query, token)

    return response.json(videos)

# from sanic_jinja2 import SanicJinja2
#
# jinja = SanicJinja2(app)
#
#
# @app.route('/')
# async def videos_view(request):
#     template = 'videos.html'
#
#     videos = await fetch_videos()
#     context = {'videos': videos}
#
#     return jinja.render(template, request, **context)
