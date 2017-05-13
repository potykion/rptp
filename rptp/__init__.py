import logging

from flask import Flask, session, request, redirect, url_for, render_template

from rptp.common.string_utils import truncate_left, truncate_right
from rptp.common.time_utils import format_seconds
from rptp.vk_api import receive_token_from_code, generate_auth_link, find_videos, DEFAULT_OFFSET, \
    receive_token_from_validation_url

app = Flask(__name__)
app.jinja_env.filters['format_seconds'] = format_seconds
app.jinja_env.filters['truncate_left'] = truncate_left
app.jinja_env.filters['truncate_right'] = truncate_right

from rptp.models import *


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


def request_access_token():
    if 'IS_HEROKU' in os.environ:
        return session.get('access_token')
    else:
        from rptp.config import TOKEN
        return TOKEN


@app.route("/")
def hello():
    token = request_access_token()

    if not token:
        code = request.args.get('code')

        if code:
            result = receive_token_from_code(code)
            app.logger.info(result)

            if 'access_token' in result:
                session.update(result)
                user = User.get_or_create(result['user_id'])
                user.update_token(result['access_token'])

            return redirect(url_for('hello'))

        auth_link = generate_auth_link()

        context = {
            'auth_url': auth_link
        }
    else:
        query = request.args.get('query')

        if not query:
            return redirect(url_for('hello', query=actress_manager.generate_actress()))

        offset = request.args.get('offset', 0, type=int)

        try:
            videos, count_ = find_videos(query, offset=offset, token=token)
        except LookupError as e:
            app.logger.info(e)
            message, error = e.args

            _process_error(error)

            return redirect(url_for('hello'))
        else:
            if not videos:
                return redirect(url_for('hello', query=actress_manager.generate_actress()))

        context = {
            'token': token,
            'query': query,
            'videos': videos,
            'count': count_,
            'offset': offset,
            'DEFAULT_OFFSET': DEFAULT_OFFSET
        }

    return render_template('video.html', **context)


def _process_error(error):
    error_code = error['error_code']

    if error_code == 5:
        session.pop('access_token')
    elif error_code == 17:
        try:
            result = receive_token_from_validation_url(error['redirect_uri'])
        except LookupError as e:
            app.logger.info(e)
            raise RuntimeError('Failed to process error!')
        else:
            session.update(result)
            user = User.get_or_create(result['user_id'])
            user.update_token(result['access_token'])
    else:
        raise ValueError('Unknown error!')
