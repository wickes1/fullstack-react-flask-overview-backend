import jwt
import os
import uuid
from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from app import db

auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route("/newuser", methods=['GET', "POST"])
def create_user():
    # if not current_user.admin:
    #     return jsonify({"message": "Cannot perform that function!"})

    data = request.get_json()
    hashsed_password = generate_password_hash(
        data["password"], method="sha256")
    new_user = User(public_id=str(uuid.uuid4()),
                    username=data["username"], password=hashsed_password, admin=data['admin'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "New user created!"})


@auth.route("/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify: Auth Info did not provided", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    user = db.session.query(User).filter_by(username=auth.username).first()
    print(user)
    print(user.password)
    if not user:
        return make_response("Could not verify: User does not exist", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({"public_id": user.public_id},
                           os.getenv("SECRET_KEY"))
        #  "exp": datetime.datetime.utcnow) + datetime.timedelta(minutes=30)
        return jsonify({"token": token})

    return make_response("Could not verify: hashed password does not match", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        else:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token, os.getenv('SECRET_KEY'), algorithms="HS256")
            current_user = db.session.query(User).filter_by(
                public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
