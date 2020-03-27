from app import db
from app.models.serializer import Serializer


class Weather(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), index=True, unique=True)
    country = db.Column(db.String(80))
    flag = db.Column(db.String(512))
    town = db.Column(db.String(80))
    tendency = db.Column(db.String(80))
    wind_speed = db.Column(db.String(20))
    temperature_min = db.Column(db.String(20))
    temperature_max = db.Column(db.String(20))
    temperature = db.Column(db.String(20))
    humidity = db.Column(db.String(40))
    clouds = db.Column(db.String(80))

    def __repr__(self):
        return '<Weather {} : {}>'.format(self.town, self.temperature)

    def serialize(self):
        return Serializer.serialize(self)
