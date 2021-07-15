from flask import Blueprint, jsonify, request
from sqlalchemy.sql import text
from .models import *
from .auth import token_required
from app import db

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def main_index():
    return 'API Page'


@api.route('/sql_query')
def sql_query():
    s = text("SELECT type, avg(eui) AS `average_eui` FROM ( SELECT `t`.`OSEBuildingID` AS `id`, `t`.`PrimaryPropertyType` AS `type`, `t2`.`electricity` / `t1`.`gfa` AS `eui` FROM `buildings` t LEFT JOIN ( SELECT `OSEBuildingID` AS `id`, SUM(`PropertyUseTypeGFA`) AS `gfa` FROM `buildings_gfa` GROUP BY `OSEBuildingID` ) t1 ON `t`.`OSEBuildingID` = `t1`.`id` LEFT JOIN ( SELECT `OSEBuildingID` AS id, value AS `electricity` FROM metrics WHERE metric = 'Electricity' ) t2 ON `t`.`OSEBuildingID` = `t2`.`id` ) GROUP BY `type`")
    results = db.engine.execute(s)
    output = []
    for result in results:
        result_data = {}
        result_data['type'] = result[0]
        result_data['avg(eui)'] = result[1]
        output.append(result_data)
    return jsonify({'res': output})


@api.route('/building_overview', methods=["POST"])
@token_required
def building_overview(current_user):
    results = db.session.query(Buildings).all()
    data = request.get_json()
    print(data)
    per_page = data['per_page']
    page = data['page'] - 1
    page_size = len(results)
    # my_list = [my_list[i:i + per_page] for i in range(0, len(my_list), per_page)][page]
    paginated_results = [results[i:i + per_page]
                         for i in range(0, page_size, per_page)][page]
    return jsonify({"res": [Buildings.serialize(paginated_result) for paginated_result in paginated_results], "page_size": page_size})


@api.route("/buildings", methods=["GET"])
@token_required
def get_all_buildings(current_user):
    # if not current_user.admin:
    #     return jsonify({"message": "Cannot perform that function!"})
    results = db.session.query(Buildings).limit(5).all()
    return jsonify({"res": [Buildings.serialize(result) for result in results]})


# @api.route("/buildings_gfa", methods=["GET"])
# # @token_required
# def get_all_buildings_gfa():
#     # if not current_user.admin:
#     #     return jsonify({"message": "Cannot perform that function!"})
#     results = db.session.query(Buildings_gfa).limit(5).all()
#     return jsonify({"res": [Buildings_gfa.serialize(result) for result in results]})


# @api.route("/energy_star_rating", methods=["GET"])
# @token_required
# def get_all_energy_star_rating(current_user):
#     results = db.session.query(Energy_star_rating).limit(5).all()
#     return jsonify({"res": [Energy_star_rating.serialize(result) for result in results]})


# @api.route("/metrics", methods=["GET"])
# @token_required
# def get_all_metrics(current_user):
#     results = db.session.query(Metrics).limit(5).all()
#     return jsonify({"res": [Metrics.serialize(result) for result in results]})
