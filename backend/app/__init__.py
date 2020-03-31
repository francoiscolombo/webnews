import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.webnews import bp as news_bp
    app.register_blueprint(news_bp)

    from app.routes.weather import bp as weather_bp
    app.register_blueprint(weather_bp)

    from app.routes.stats import bp as stats_bp
    app.register_blueprint(stats_bp)

    if not app.debug and not app.testing:
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask app name is {}'.format(app.name))
        app.logger.info('FCWebNews API ready to process requests')

    return app
