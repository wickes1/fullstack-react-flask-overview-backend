from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import *

db = SQLAlchemy()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')


def model_exists(model_class):
    engine = db.get_engine(bind=model_class.__bind_key__)
    return model_class.metadata.tables[model_class.__tablename__].exists(engine)


def create_app(config=None):
    app = Flask(__name__, static_url_path="", static_folder="build")
    CORS(app)
    # app.config.from_object('config.ProductionConfig')
    # app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)

    # Serve React App
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + "/" + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    # if not model_exists(User):
    #     User.__table__.create(db.session.bind)

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


if __name__ == "__main__":
    app = create_app()
    app.run(use_reloader=True, port=5000, threaded=True)
