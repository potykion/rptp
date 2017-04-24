import logging
import os

import requests
from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

from rptp.vk_api import find_videos, generate_auth_link, generate_token_receive_link

DEFAULT_QUERY = 'Jessie Rogers'
DEFAULT_OFFSET = 20

app = Flask(__name__)

if 'IS_HEROKU' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)
else:
    # local dev
    pass


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


def generate_actress():
    return 'sample text'


@app.route("/")
def hello():
    token = session.get('access_token')

    if not token:
        code = request.args.get('code')

        if code:
            token_link = generate_token_receive_link(code)
            result = requests.get(token_link).json()
            app.logger.info(result)
            session.update(result)
            return redirect(url_for('hello'))

        auth_link = generate_auth_link()

        context = {
            'auth_url': auth_link
        }

    else:
        if request.args.get('refresh'):
            query = generate_actress()
        else:
            query = request.args.get('query', DEFAULT_QUERY)

        offset = request.args.get('search', 0, type=int)

        try:
            videos, count_ = find_videos(query, offset=offset, token=token)
            app.logger.info(videos[0])
        except Exception as e:
            app.logger.info(type(e))
            app.logger.info(e)
            videos = []
        else:
            if not videos:
                return redirect(url_for('hello', refresh=1))

        context = {
            'token': token,
            'query': query,
            # 'count': count_,
            'videos': videos,
            'offset': offset,
            'DEFAULT_OFFSET': DEFAULT_OFFSET
        }

    return render_template('video.html', **context)


if __name__ == "__main__":
    app.run()
