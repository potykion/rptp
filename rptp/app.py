import json

from sanic import Sanic
from sanic.response import json as json_response
from sanic_jinja2 import SanicJinja2

from rptp.config import TEMPLATES_DIR
from rptp.getters import get_videos

app = Sanic(__name__)
app.static('/static', './static')
jinja = SanicJinja2(app, pkg_path=TEMPLATES_DIR)


@app.route('/api/videos')
async def video_api_view(request):
    query = request.args.get('query')
    token = request.headers.get('authorization') or request.args.get('token')

    videos = await get_videos(query, token)

    return json_response(videos)


@app.route('/videos')
async def videos_template_view(request):
    template = 'videos.html'

    query = request.args.get('query')

    response = await video_api_view(request)
    videos = json.loads(response.body)

    context = {'query': query, 'videos': videos}

    return jinja.render(template, request, **context)


@app.route('/index')
async def index_template_view(request):
    template = 'index.html'

    context = {}

    return jinja.render(template, request, **context)
