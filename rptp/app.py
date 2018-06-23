import json

from jinja2 import Environment, select_autoescape, FileSystemLoader
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sanic import Sanic, response

from rptp.async_actress import pick_random, mark_has_videos
from rptp.auth import VKResponseAuthorizer, extract_auth_data
from rptp.config import TEMPLATES_DIR, STATIC_DIR, MONGO_DB, MONGO_URL
from rptp.decorators import browser_authorization_required, required_query_params, api_authorization_required
from rptp.getters import get_videos

app = Sanic(__name__)
app.static('/static', STATIC_DIR)

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)

db: AsyncIOMotorDatabase


@app.listener('before_server_start')
def init(sanic, loop):
    global db

    client = AsyncIOMotorClient(MONGO_URL)
    db = client[MONGO_DB]


@app.route('/api/videos')
@api_authorization_required()
async def video_api_view(request):
    query = request.args.get('query')
    count = request.args.get('count', 100)
    token = extract_auth_data(request)

    videos = await get_videos(query, token, count=count)

    return response.json(videos)


@app.route('/api/pick_random')
@api_authorization_required()
async def pick_random_api_view(request):
    actress = await pick_random(db, with_id=False)
    return response.json(actress)


@app.route('/api/report')
@api_authorization_required()
@required_query_params(['query'])
async def report_api_view(request):
    query = request.args.get('query')
    await mark_has_videos(db, query, False)
    return response.json({
        'success': True
    })


@app.route('/videos')
@browser_authorization_required()
@required_query_params(['query'])
async def videos_template_view(request):
    query = request.args.get('query')

    api_response = await video_api_view(request)
    videos = json.loads(api_response.body)

    template = jinja_env.get_template('videos.html')
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

        authorizer = VKResponseAuthorizer()
        response_ = await authorizer.authorize_response(response_, code)

    elif extract_auth_data(request):
        rendered = await template.render_async()
        response_ = response.html(rendered)
    else:
        authorizer = VKResponseAuthorizer()
        response_ = await authorizer.create_authorization_response(template)

    return response_
