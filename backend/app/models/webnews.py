from app import db
from datetime import datetime
from app.models.serializer import Serializer


class WebNewsCategory(db.Model, Serializer):
    __tablename__ = 'web_news_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    news = db.relationship('WebNews', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<WebNewsCategory {}>'.format(self.name)

    def serialize(self):
        return Serializer.serialize(self)


class WebNews(db.Model, Serializer):
    __tablename__ = 'web_news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, unique=True)
    author = db.Column(db.String(64), index=True)
    photo = db.Column(db.String(256))
    source = db.Column(db.String(256))
    is_headline = db.Column(db.String(3), default='no')
    is_top_story = db.Column(db.String(3), default='no')
    date_publish = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String(2048))
    category_id = db.Column(db.Integer, db.ForeignKey('web_news_category.id'))
    keywords = db.relationship('WebNewsKeyword', secondary='link')

    def __repr__(self):
        return '<WebNews {}>'.format(self.title)

    def serialize(self):
        return {
            'id': str(self.id),
            'title': str(self.title),
            'author': str(self.author),
            'photo': str(self.photo),
            'source': str(self.source),
            'is_headline': str(self.is_headline),
            'is_top_story': str(self.is_headline),
            'date_publish': str(self.date_publish),
            'content': str(self.content),
            'category': str(self.category_id),
            'tags': [str(x) for x in self.keywords]
        }


class WebNewsKeyword(db.Model, Serializer):
    __tablename__ = 'web_news_keyword'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), index=True, unique=True)
    related = db.relationship('WebNews', secondary='link')

    def __repr__(self):
        return '<WebNewsKeyword {}>'.format(self.tag)

    def serialize(self):
        return Serializer.serialize(self)


class Link(db.Model):
    __tablename__ = 'link'
    web_news_id = db.Column(db.Integer, db.ForeignKey('web_news.id'), primary_key=True)
    web_news_keyword_id = db.Column(db.Integer, db.ForeignKey('web_news_keyword.id'), primary_key=True)
