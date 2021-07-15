from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import *

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__, static_url_path="", static_folder="build")
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)

    from .auth import auth
    app.register_blueprint(auth)

    from .api import api
    app.register_blueprint(api)

    from .pages import page
    app.register_blueprint(page)

    # admin = User(name='admin', password='123456', admin=True)
    # db.session.add(admin)
    # db.session.commit()

    # app.run(use_reloader=True, port=5000, threaded=True)
    return app
