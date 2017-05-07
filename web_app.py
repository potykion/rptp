import logging
import os

from flask import Flask, request, redirect, url_for, render_template, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from rptp.common.utils import format_seconds, truncate_left, truncate_right
from rptp.vk_api import find_videos, generate_auth_link, DEFAULT_OFFSET, \
    receive_token_from_code

app = Flask(__name__)
app.jinja_env.filters['format_seconds'] = format_seconds
app.jinja_env.filters['truncate_left'] = truncate_left
app.jinja_env.filters['truncate_right'] = truncate_right

if 'IS_HEROKU' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    from rptp.prod.models import ActressManager, User
else:
    from rptp.local.models import ActressManager

actress_manager = ActressManager()


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
        if request.args.get('refresh'):
            query = actress_manager.generate_actress()
        else:
            query = request.args.get('query', actress_manager.generate_actress())

        offset = request.args.get('search', 0, type=int)

        try:
            videos, count_ = find_videos(query, offset=offset, token=token)
        except LookupError as e:
            app.logger.info(e)
            message, error = e.args

            if error['error_code'] == 5:
                session.pop('access_token')
                return redirect(url_for('hello'))

            videos, count_ = [], 0
        else:
            if not videos:
                return redirect(url_for('hello'))

        context = {
            'token': token,
            'query': query,
            'videos': videos,
            'count': count_,
            'offset': offset,
            'DEFAULT_OFFSET': DEFAULT_OFFSET
        }

    return render_template('video.html', **context)


if __name__ == "__main__":
    app.run()
