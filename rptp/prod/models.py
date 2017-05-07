from rptp.common.models import ActressProxy
from web_app import db

"""
For new models:
$ heroku run python
>>> from web_app import db
>>> db.create_all()
"""


class Actress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer, default=0)
    name = db.Column(db.String(100))
    image = db.Column(db.String(100))
    debut_year = db.Column(db.Integer)
    url = db.Column(db.String(100))

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    @classmethod
    def create_from_json(cls, actress_json):
        """
        Create actress from json.
        :param actress_json: Actress json, example:
        {
            "priority": 0,
            "name": "Kandi Quinn",
            "image": "/images/models/kandi-quinn.jpg",
            "debut_year": 2017,
            "url": "/model/kandi-quinn.html"
        }

        :return: New actress
        """

        exists = db.session.query(db.exists().where(Actress.url == actress_json['url'])).scalar()
        if not exists:
            actress = cls(**actress_json)
            db.session.add(actress)
            db.session.commit()
            return actress


class ActressManager(ActressProxy):
    def fetch(self):
        return Actress.query.all()

    def serialize(self, actress):
        return {
            "priority": actress.priority,
            "name": actress.name,
            "image": actress.image,
            "debut_year": actress.debut_year,
            "url": actress.url
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    @classmethod
    def get_or_create(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()

        if not user:
            user = cls(user_id=user_id)
            db.session.add(user)
            db.session.commit()

        return user

    def update_token(self, token):
        self.access_token = token
        db.session.commit()
