from app import db
from app.models.serializer import Serializer
import jwt
from flask import current_app
from time import time


class Auth(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Auth {}>'.format(self.application)

    def serialize(self):
        return Serializer.serialize(self)

    def get_token(self, expires_in=31557600):
        # token alive for one year
        return jwt.encode(
            {
                'application': self.id,
                'expires': time() + expires_in
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['application']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.DecodeError:
            return None
        except jwt.InvalidTokenError:
            return None
        return Auth.query.get(id)
