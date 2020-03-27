import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    PRODUCTION_MODE = os.environ.get('PRODUCTION_MODE') or 'no'
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''
    X_RAPID_API_KEY = os.environ.get('X_RAPID_API_KEY') or ''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'backend.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
