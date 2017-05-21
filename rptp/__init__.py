import logging
import os
from functools import wraps

from flask import Flask, session, request, redirect, url_for, render_template

from rptp.common.string_utils import truncate_left, truncate_right
from rptp.common.time_utils import format_seconds
from rptp.common.web_utils import is_mobile_user_agent
from rptp.vk_api import receive_token_from_code, generate_auth_link, \
    receive_token_from_validation_url, search_videos, request_adult_videos, VIDEO_COUNT

app = Flask(__name__)
app.jinja_env.filters['format_seconds'] = format_seconds
app.jinja_env.filters['truncate_left'] = truncate_left
app.jinja_env.filters['truncate_right'] = truncate_right

from rptp.models import *

if 'IS_HEROKU' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']
else:
    from rptp.local_config import *

    app.secret_key = SECRET_KEY


@app.before_first_request
def app_setup():
    if 'IS_HEROKU' in os.environ:
        return
    else:
        session['access_token'] = TOKEN


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('auth_view'))
        return f(*args, **kwargs)

    return wrapper


@app.route('/videos')
@token_required
def videos_view():
    """
    View for showing and querying videos .

    """
    query = request.args.get('query')
    if not query:
        return redirect(url_for('videos_view', query=actress_manager.generate_actress()))

    offset = request.args.get('offset', 0, type=int)

    try:
        videos, new_offset = request_adult_videos(query, offset)
    except LookupError as e:
        app.logger.info(e)
        raise e
    else:
        if not videos:
            # no videos found try another actress
            return redirect(url_for('videos_view', query=actress_manager.generate_actress()))

    context = {
        'videos': videos,
        'query': query,
        'offset': new_offset,
        'VIDEO_COUNT': VIDEO_COUNT,
        'is_mobile': is_mobile_user_agent(request)
    }

    return render_template('video.html', **context)


@app.route('/auth')
def auth_view():
    code = request.args.get('code')

    if code:
        result = receive_token_from_code(code)
        app.logger.info(result)

        if 'access_token' in result:
            session.update(result)
            user = User.get_or_create(result['user_id'])
            user.update_token(result['access_token'])

        return redirect(url_for('main_view'))

    return render_template('auth.html', auth_url=generate_auth_link())


@app.route("/")
def main_view():
    return redirect(url_for('videos_view', query=actress_manager.generate_actress()))
