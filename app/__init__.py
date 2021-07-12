from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import *

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)

    from .pages import page
    from .api import api
    app.register_blueprint(page)
    app.register_blueprint(api)

    # admin = User(name='admin', password='123456', admin=True)
    # db.session.add(admin)
    # db.session.commit()

    # app.run(use_reloader=True, port=5000, threaded=True)
    return app
