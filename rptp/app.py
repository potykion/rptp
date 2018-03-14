import json

from jinja2 import Environment, select_autoescape, FileSystemLoader
from sanic import Sanic, response

from rptp.auth import VKAuthorizer, extract_auth_data
from rptp.config import TEMPLATES_DIR, STATIC_DIR
from rptp.decorators import browser_authorization_required
from rptp.getters import get_videos

app = Sanic(__name__)
app.static('/static', STATIC_DIR)

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)


@app.route('/api/videos')
async def video_api_view(request):
    query = request.args.get('query')
    token = extract_auth_data(request)

    videos = await get_videos(query, token)

    return response.json(videos)


@app.route('/videos')
@browser_authorization_required()
async def videos_template_view(request):
    template = jinja_env.get_template('videos.html')

    query = request.args.get('query')

    response_ = await video_api_view(request)
    videos = json.loads(response_.body)

    context = {'query': query, 'videos': videos}

    rendered = await template.render_async(**context)
    return response.html(rendered)


@app.route('/')
@app.route('/index')
async def index_template_view(request):
    template = jinja_env.get_template('index.html')

    code = request.args.get('code')
    if code:
        rendered = await template.render_async()
        response_ = response.html(rendered)

        authorizer = VKAuthorizer()
        response_ = await authorizer.authorize_response(response_, code)

        return response_
    elif extract_auth_data(request):
        rendered = await template.render_async()
        response_ = response.html(rendered)
    else:
        authorizer = VKAuthorizer()
        auth_link = authorizer.generate_auth_link()
        context = {'auth_link': auth_link}

        rendered = await template.render_async(**context)
        response_ = response.html(rendered)

    return response_
