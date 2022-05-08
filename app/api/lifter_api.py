"""
lifter_api.py

Handles logic and routing for the gym database and all tables
within. (as of 5/7: gym_members, workouts, exercise_sets are the table names)
"""

from flask import g, request, jsonify, Blueprint

from models.gym_member import *
from models.weight_set import *
from models.workout import *

lifter_api_blueprint = Blueprint("lifter_api_blueprint", __name__)

@lifter_api_blueprint.route('/api/v1/members/', defaults={'gym_id':None}, methods=["GET"])
@lifter_api_blueprint.route('/api/v1/members/<int:gym_id>/', methods=["GET"])
def get_members(gym_id):
    """
    get_members can be used in two forms currently:
    * /api/v1/members/ - get all members
    * /api/v1/members/3 - get member with id 3 (or other valid id)
    """

    memberDB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)

    result = None

    if gym_id is None:
        result = memberDB.select_all_members()

    else:
        result = memberDB.select_individual_member(gym_id)

    return jsonify({"status": "success", "members": result}), 200
