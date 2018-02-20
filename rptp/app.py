import json

from sanic import Sanic
from sanic.response import json as json_response
from sanic_jinja2 import SanicJinja2

from rptp.config import TEMPLATES_DIR
from rptp.getters import get_videos

app = Sanic(__name__)
jinja = SanicJinja2(app, pkg_path=TEMPLATES_DIR)


@app.route('/api/videos')
async def video_api_view(request):
    query = request.args.get('query')
    token = request.headers.get('authorization') or request.args.get('token')

    videos = await get_videos(query, token)

    return json_response(videos)


@app.route('/videos')
async def videos_view(request):
    template = 'videos.html'

    response = await video_api_view(request)
    videos = json.loads(response.body)
    context = {'videos': videos}

    return jinja.render(template, request, **context)
