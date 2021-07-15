from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import *

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__, static_url_path="", static_folder="build")
    CORS(app)
    # app.config.from_object('config.ProductionConfig')
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)

    # Serve React App
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + "/" + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

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
