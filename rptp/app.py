import json

from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2

from rptp.config import TEMPLATES_DIR
from rptp.getters import get_videos
from rptp import vk_api

app = Sanic(__name__)
app.static('/static', './static')
jinja = SanicJinja2(app, pkg_path=TEMPLATES_DIR)


@app.route('/api/videos')
async def video_api_view(request):
    query = request.args.get('query')
    token = request.headers.get('authorization') or request.args.get('token')

    videos = await get_videos(query, token)

    return response.json(videos)


@app.route('/videos')
async def videos_template_view(request):
    template = 'videos.html'

    query = request.args.get('query')

    response_ = await video_api_view(request)
    videos = json.loads(response_.body)

    context = {'query': query, 'videos': videos}

    return jinja.render(template, request, **context)


@app.route('/index')
async def index_template_view(request):
    template = 'index.html'
    context = {}

    code = request.args.get('code')

    if code:
        token_data = await vk_api.request_token_data(code)
        # response_ = response.redirect('/videos')
        response_ = response.text('oppa')
        response_.cookies['access_token'] = token_data['access_token']
        response_.cookies['user_id'] = str(token_data['user_id'])
        return response_
    else:

        auth_link = vk_api.generate_auth_link()
        context.update({'auth_link': auth_link})

        return jinja.render(template, request, **context)
