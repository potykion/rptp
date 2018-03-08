import json

from jinja2 import Environment, select_autoescape, FileSystemLoader
from sanic import Sanic, response

from rptp.auth import VKAuthorizer
from rptp.config import TEMPLATES_DIR
from rptp.cookie import save_token_data, has_token
from rptp.getters import get_videos

app = Sanic(__name__)
app.static('/static', './static')
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)


@app.route('/api/videos')
async def video_api_view(request):
    query = request.args.get('query')
    token = request.headers.get('authorization') or request.args.get('token')

    videos = await get_videos(query, token)

    return response.json(videos)


@app.route('/videos')
async def videos_template_view(request):
    template = jinja_env.get_template('videos.html')

    query = request.args.get('query')

    response_ = await video_api_view(request)
    videos = json.loads(response_.body)

    context = {'query': query, 'videos': videos}

    rendered = await template.render_async(**context)
    return response.html(rendered)


@app.route('/index')
async def index_template_view(request):
    template = jinja_env.get_template('index.html')
    context = {}

    code = request.args.get('code')
    authorizer = VKAuthorizer()

    if code:
        user_id, token = await authorizer.auth(code)
        rendered = await template.render_async(**context)
        response_ = response.html(rendered)
        response_ = save_token_data(response_, user_id, token)
        return response_
    elif has_token(request):
        rendered = await template.render_async(**context)
        response_ = response.html(rendered)
        return response_
    else:
        auth_link = authorizer.generate_auth_link()
        context.update({'auth_link': auth_link})
        rendered = await template.render_async(**context)
        response_ = response.html(rendered)
        return response_
