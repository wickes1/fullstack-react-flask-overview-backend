import os
from flask import Blueprint
from flask import jsonify
from .models import *
from app import db


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def main_index():
    return 'API Page'


@api.route("/buildings", methods=["GET"])
def get_all_buildings():
    results = db.session.query(Buildings).limit(5).all()
    return jsonify({"res": [Buildings.serialize(result) for result in results]})


@api.route("/buildings_gfa", methods=["GET"])
def get_all_buildings_gfa():
    results = db.session.query(Buildings_gfa).limit(5).all()
    return jsonify({"res": [Buildings_gfa.serialize(result) for result in results]})


@api.route("/energy_star_rating", methods=["GET"])
def get_all_energy_star_rating():
    results = db.session.query(Energy_star_rating).limit(5).all()
    return jsonify({"res": [Energy_star_rating.serialize(result) for result in results]})


@api.route("/metrics", methods=["GET"])
def get_all_metrics():
    results = db.session.query(Metrics).limit(5).all()
    return jsonify({"res": [Metrics.serialize(result) for result in results]})
