import requests
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.weather import Weather
from app.models.auth import Auth
from config import Config
from requests.exceptions import HTTPError

bp = Blueprint('weather', __name__)


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Invalid request'}), 400)


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


@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@bp.route('/api/v1.0/weather_ips', methods=['GET'])
def get_all_ips():
    all_records = Weather.query.all()
    if all_records:
        all_ips = [{'ip': i.ip} for i in all_records]
        return jsonify(all_ips)
    return jsonify([])


@bp.route('/api/v1.0/weather/<ip_wan>', methods=['GET'])
def get_weather(ip_wan):
    if ip_wan:
        print('IP wan is {}'.format(ip_wan))
        w = Weather.query.filter_by(ip=ip_wan).first()
        if not w:
            abort(404)
        return jsonify(w.serialize())
    return jsonify([])


@bp.route('/api/v1.0/weather', methods=['PUT'])
def update_weather():
    if not request.json or 'ip' not in request.json:
        abort(400)
    # okay, we have the IP of the customer, so now we need to call a geo location service to retrieve the details
    headers = {
        'x-rapidapi-host': "ip1.p.rapidapi.com",
        'x-rapidapi-key': Config.X_RAPID_API_KEY
    }
    url = "https://ip1.p.rapidapi.com/" + request.json['ip']
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        country = response.json()['country']
        town = response.json()['city']
        flag = response.json()['flag']['svg']
        country_code = response.json()['country_code']
        postal_code = response.json()['postal']
        latitude = str(response.json()['latitude'])
        longitude = str(response.json()['longitude'])
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': Config.X_RAPID_API_KEY
        }
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"
        querystring = {
            'q': '{},{}'.format(town, country_code),
            'units': 'metric',
            'lat': latitude,
            'lon': longitude,
            'lang': "en",
            'cnt': "1",
            'zip': postal_code
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        resp = response.json()['list'][0]
        response.raise_for_status()
        temperature_min = resp['main']['temp_min']
        temperature_max = resp['main']['temp_max']
        temperature = resp['main']['temp']
        humidity = resp['main']['humidity']
        tendency = resp['weather'][0]['description']
        clouds = resp['weather'][0]['main']
        wind_speed = resp['wind']['speed']
        w = Weather.query.filter_by(ip=request.json['ip']).first()
        if not w:
            w = Weather()
            w.ip = request.json['ip']
            w.country = country
            w.flag = flag
            w.town = town
            w.tendency = tendency
            w.wind_speed = wind_speed
            w.temperature_min = temperature_min
            w.temperature_max = temperature_max
            w.temperature = temperature
            w.humidity = humidity
            w.clouds = clouds
            db.session.add(w)
        else:
            setattr(w, 'country', country)
            setattr(w, 'flag', flag)
            setattr(w, 'town', town)
            setattr(w, 'tendency', tendency)
            setattr(w, 'wind_speed', wind_speed)
            setattr(w, 'temperature', temperature)
            setattr(w, 'temperature_min', temperature_min)
            setattr(w, 'temperature_max', temperature_max)
            setattr(w, 'humidity', humidity)
            setattr(w, 'clouds', clouds)
        db.session.commit()
        return jsonify({'ip': request.json['ip']}), 201
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    abort(400)


@bp.route('/api/v1.0/weather/<ip_wan>', methods=['DELETE'])
def delete_weather(ip_wan):
    w = Weather.query.filter_by(ip=ip_wan).first()
    if not w:
        abort(404)
    db.session.delete(w)
    db.session.commit()
    return jsonify({'result': True})
