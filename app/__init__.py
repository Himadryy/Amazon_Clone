from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    login_manager.login_view = "auth.signin"
    login_manager.login_message = "Please sign in to access this page."

    from app.routes import products, cart, auth, main, api

    app.register_blueprint(products.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get(user_id)

    @app.context_processor
    def inject_translations():
        from app.utils.translations import TRANSLATIONS

        return dict(TRANSLATIONS=TRANSLATIONS)

    return app
