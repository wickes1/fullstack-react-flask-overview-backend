import os
import jwt
import datetime
import uuid
from flask import Blueprint,  request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import *
from .auth import token_required
from app import db


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def main_index():
    return 'API Page'


@api.route("/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    user = db.session.query(User).filter_by(name=auth.username).first()

    if not user:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({"public_id": user.public_id, "exp": datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, os.getenv("SECRET_KEY"))

        return jsonify({"token": token})

    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})


@api.route("/newuser", methods=["POST"])
def create_user():
    # if not current_user.admin:
    #     return jsonify({"message": "Cannot perform that function!"})

    data = request.get_json()
    hashsed_password = generate_password_hash(
        data["password"], method="sha256")
    new_user = User(public_id=str(uuid.uuid4()),
                    name=data["name"], password=hashsed_password, admin=data['admin'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "New user created!"})


@api.route("/buildings", methods=["GET"])
@token_required
def get_all_buildings(current_user):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})
    results = db.session.query(Buildings).limit(5).all()
    return jsonify({"res": [Buildings.serialize(result) for result in results]})


@api.route("/buildings_gfa", methods=["GET"])
# @token_required
def get_all_buildings_gfa():
    # if not current_user.admin:
    #     return jsonify({"message": "Cannot perform that function!"})
    results = db.session.query(Buildings_gfa).limit(5).all()
    return jsonify({"res": [Buildings_gfa.serialize(result) for result in results]})


@api.route("/energy_star_rating", methods=["GET"])
@token_required
def get_all_energy_star_rating(current_user):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})
    results = db.session.query(Energy_star_rating).limit(5).all()
    return jsonify({"res": [Energy_star_rating.serialize(result) for result in results]})


@api.route("/metrics", methods=["GET"])
@token_required
def get_all_metrics(current_user):
    if not current_user.admin:
        return jsonify({"message": "Cannot perform that function!"})
    results = db.session.query(Metrics).limit(5).all()
    return jsonify({"res": [Metrics.serialize(result) for result in results]})
