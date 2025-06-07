from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if config:
        app.config.update(config)

    db.init_app(app)
    login_manager.init_app(app)

    # register blueprints
    from .auth import auth_bp
    from .assets import asset_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(asset_bp)

    return app


def init_db(app):
    """Create database tables."""
    with app.app_context():
        db.create_all()
