from flask import Blueprint, jsonify
from app import db
from app.models.webnews import WebNewsCategory, WebNews, WebNewsKeyword

bp = Blueprint('stats', __name__)


@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@bp.route('/api/v1.0/stats', methods=['GET'])
def get_stats():
    return jsonify({'count': {
        'categories': str(db.session.query(WebNewsCategory.id).count()),
        'news': str(db.session.query(WebNews.id).count()),
        'tags': str(db.session.query(WebNewsKeyword.id).count()),
    }})
