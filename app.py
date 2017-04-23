import logging
import os

from flask import Flask, request, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from rptp.vk_api import find_videos

DEFAULT_QUERY = 'Jessie Rogers'
DEFAULT_OFFSET = 20

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


def generate_actress():
    return 'Ukraine'


@app.before_first_request
def setup_logging():
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)


@app.route("/")
def hello():
    if request.args.get('refresh'):
        query = generate_actress()
    else:
        query = request.args.get('query', DEFAULT_QUERY)

    offset = request.args.get('search', 0, type=int)

    try:
        count_, videos = find_videos(query, offset=offset).values()
    except Exception as e:
        app.logger.info(e)
        videos = []
    else:
        if not videos:
            return redirect(url_for('hello', refresh=1))

    context = {
        'query': query,
        # 'count': count_,
        'videos': videos,
        'offset': offset,
        'DEFAULT_OFFSET': DEFAULT_OFFSET
    }

    return render_template('video.html', **context)


if __name__ == "__main__":
    app.run()
