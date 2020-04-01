from dateutil.parser import isoparse
from flask import Blueprint, jsonify, abort, make_response, request
from flask_cors import cross_origin
from config import Config
from app import db
from app.models.webnews import WebNewsCategory, WebNews, WebNewsKeyword
from app.models.auth import Auth
from datetime import datetime, timedelta

bp = Blueprint('webnews', __name__)


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Invalid request'}), 400)


@bp.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal server error: {}'.format(error)}), 500)


@bp.before_request
def before_request_auth():
    if Config.PRODUCTION_MODE == 'yes':
        if request.method != 'OPTIONS':
            if 'application' in request.headers and 'token' in request.headers:
                a = Auth.verify_token(request.headers['token'])
                if a is None:
                    abort(401)
                if a.application.lower() != request.headers['application'].lower():
                    abort(403)
            else:
                abort(401)


@bp.route('/api/v1.0/categories/<cat_list>', methods=['GET'])
@cross_origin()
def get_categories(cat_list):
    selected_categories = cat_list.split(',')
    categories = []
    all_categories = WebNewsCategory.query.all()
    # we are filtering for the news that have at least 4 news related, we skip the other categories
    for c in all_categories:
        if c.name in selected_categories:
            cat_news = WebNews.query.filter_by(category_id=c.id).order_by(WebNews.date_publish.desc())
            if cat_news.count() >= 4:
                news = [
                    {
                        'id': cn.id,
                        'title': cn.title,
                        'source': cn.source,
                        'photo': cn.photo,
                        'content': cn.content,
                        'date_publish': cn.date_publish,
                        'tag': [t.tag for t in cn.keywords if ' ' not in t.tag]
                    }
                    for cn in cat_news
                ]
                categories.append({
                    'id': c.id,
                    'title': c.name,
                    'primary': news[0],
                    'news': [news[1], news[2], news[3]]
                })
    return jsonify(categories)


@bp.route('/api/v1.0/keywords', methods=['GET'])
@cross_origin()
def get_keywords():
    # note: only send back keywords with more than 3 news related
    all_keywords = WebNewsKeyword.query.all()
    keywords = [
        {'id': k.id, 'label': k.tag, 'count': len(k.related)}
        for k in all_keywords if (" " not in k.tag) and (len(k.related) > 3)
    ]
    return jsonify(keywords)


@bp.route('/api/v1.0/newsbycategory/<cat_id>', methods=['GET'])
@cross_origin()
def get_news_by_category(cat_id):
    c = WebNewsCategory.query.get(int(cat_id))
    if c:
        all_news = [n.serialize for n in c.news]
        return jsonify({'news': all_news})
    return jsonify({'news': []})


@bp.route('/api/v1.0/newsbykeyword/<keyword_id>', methods=['GET'])
@cross_origin()
def get_news_by_keyword(keyword_id):
    k = WebNewsKeyword.query.get(int(keyword_id))
    if k:
        all_news = [n.serialize for n in k.related]
        return jsonify({'news': all_news})
    return jsonify({'news': []})


@bp.route('/api/v1.0/newsbyauthor/<name>', methods=['GET'])
@cross_origin()
def get_news_by_author(name):
    all_news = WebNews.query.filter_by(author=name).order_by(WebNews.date_publish.desc())
    if all_news:
        return jsonify({'news': [n.serialize for n in all_news]})
    return jsonify({'news': []})


@bp.route('/api/v1.0/top_stories', methods=['GET'])
@cross_origin()
def get_top_stories():
    all_news = WebNews.query.filter_by(is_top_story='yes').order_by(WebNews.date_publish.desc())
    if all_news:
        # return no more than 10
        top_stories = [{'id': 0, 'title': n.title, 'source': n.source, 'photo': n.photo} for n in all_news[0:9]]
        ind = 1
        for t in top_stories:
            t['id'] = ind
            ind = ind + 1
        return jsonify(top_stories)
    return jsonify([])


@bp.route('/api/v1.0/headlines/<count>', methods=['GET'])
@cross_origin()
def get_headlines(count):
    all_news = WebNews.query.filter_by(is_headline='yes').order_by(WebNews.date_publish.desc())
    if all_news:
        # return no more than 'count'
        headlines = [{'id': n.id, 'title': n.title, 'source': n.source} for n in all_news[0:int(count)]]
        return jsonify(headlines)
    return jsonify([])


@bp.route('/api/v1.0/latest_news/<page>', methods=['GET'])
@cross_origin()
def get_latest_news(page):
    one_weeks_ago = datetime.utcnow() - timedelta(weeks=1)
    all_news = db.session.query(WebNews).filter(
        WebNews.date_publish > one_weeks_ago
    ).order_by(
        WebNews.date_publish.desc()
    ).paginate(
        int(page), 10, False
    )
    if all_news:
        news = [
            {
                'id': n.id,
                'title': n.title,
                'source': n.source,
                'photo': n.photo,
                'author': n.author,
                'date_publish': n.date_publish,
                'content': n.content
            }
            for n in all_news.items
        ]
        return jsonify(news)
    return jsonify([])


@bp.route('/api/v1.0/webnews', methods=['POST'])
@cross_origin()
def create_webnews():
    if not request.json or 'title' not in request.json or 'category' not in request.json:
        abort(400)
    # check if category exists, if not create it
    news_category = str(request.json['category']).title()
    c = WebNewsCategory.query.filter_by(name=news_category).first()
    if not c:
        c = WebNewsCategory()
        c.name = news_category
        db.session.add(c)
        db.session.commit()
    # check if the news exists already (which means if we have exactly the same title, case sensitive)
    news_title = ascii(request.json['title'])
    n = WebNews.query.filter_by(title=news_title).first()
    if not n:
        # okay it does not exists yet, so we have to create it...
        n = WebNews()
        n.category = c
        n.title = news_title
        n.source = request.json['source'] or ''
        n.author = request.json['author'] or 'Unknown'
        n.content = ascii(request.json['content']) or 'No more information...'
        n.photo = request.json['photo'] or ''
        n.is_headline = request.json['is_headline'] or 'no'
        n.is_top_story = request.json['is_top_story'] or 'no'
        n.date_publish = isoparse(request.json['date_publish'])
        db.session.add(n)
        db.session.commit()
        # but that's not all, we have to process the keywords list!
        if 'keywords' in request.json:
            if str(request.json['keywords']) != '':
                kw = str(request.json['keywords']).split(';')
                for k in kw:
                    value = k.strip().upper()
                    t = WebNewsKeyword.query.filter_by(tag=value).first()
                    if not t:
                        t = WebNewsKeyword()
                        t.tag = value
                        db.session.add(t)
                        db.session.commit()
                    n.keywords.append(t)
                    db.session.commit()
        return jsonify({'webnews': n.serialize()}), 201
    return jsonify({'webnews': n.serialize()}), 200
