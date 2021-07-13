import jwt
import os
from flask import request, jsonify
from functools import wraps
from .models import User
from app import db


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
