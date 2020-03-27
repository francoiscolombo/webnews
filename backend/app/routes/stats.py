from flask import Blueprint, jsonify
from flask_cors import CORS
from app import db
from app.models.webnews import WebNewsCategory, WebNews, WebNewsKeyword

bp = Blueprint('stats', __name__)
CORS(bp)


@bp.route('/api/v1.0/stats', methods=['GET'])
def get_stats():
    return jsonify({'count': {
        'categories': str(db.session.query(WebNewsCategory.id).count()),
        'news': str(db.session.query(WebNews.id).count()),
        'tags': str(db.session.query(WebNewsKeyword.id).count()),
    }})
