import os

from flask_sqlalchemy import SQLAlchemy

from rptp import app

if 'IS_HEROKU' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)

    from rptp.prod.models import ActressManager, User
else:
    from rptp.local.models import ActressManager

actress_manager = ActressManager()
