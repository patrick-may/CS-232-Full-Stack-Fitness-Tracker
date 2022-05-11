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
def read_members(gym_id):
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

@lifter_api_blueprint.route('/api/v1/members/', methods=["POST"])
def create_member():
    new_member = Gym_Member(request.json["name"], request.json["age"], request.json["sex"])

    member_DB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    member_DB.insert_individual_member(new_member)

    return jsonify( {"status":"success", "user_id":new_member.gym_id} ), 200

@lifter_api_blueprint.route('/api/v1/members/', defaults={'gym_id':None}, methods=["DELETE"])
@lifter_api_blueprint.route('/api/v1/members/<int:gym_id>/', methods=["DELETE"])
def delete_members(gym_id):
    memberDB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    result = None

    if gym_id is None:
        all_mems = memberDB.select_all_members()

        for mem in all_mems:
            memberDB.delete_member(mem["gym_id"])
        
        return jsonify({"status": "success", "deleted": all_mems}), 200
    else:
        member = memberDB.select_individual_member(gym_id)
        memberDB.delete_member(gym_id)
    
    return jsonify({"status": "success", "deleted": member}), 200
        
@lifter_api_blueprint.route("/api/v1/<int:gym_id>/workouts/", methods=["POST"])
def add_workout(gym_id):
    db = WorkoutDB(g.mysql_db, g.mysql_cursor)

    create_id = request.json["gym_id"]
    create_date = request.json["workout_date"]
    create_duration = request.json["duration"]
    create_exercises_dict = request.json["exercises"]
    set_list = []
    for exercise_dicts in create_exercises_dict:
        set_list.append(Weight_Set(exercise_dicts["gym_id"], exercise_dicts["machine_name"], exercise_dicts["exercise_date"], exercise_dicts["reps"], exercise_dicts["weight"]))

    new_workout = Workout(create_id, create_date, create_duration, set_list)

    db.insert_workout(new_workout)

    return jsonify({"status":"success", "inserted":db.select_workout(create_id, create_date)}), 200

@lifter_api_blueprint.route('/api/v1/workouts/', methods=["GET"])
def read_workouts(gym_id):

    workoutDB = WorkoutDB(g.mysql_db, g.mysql_cursor)

    result = None

    result = WorkoutDB.select_all_workouts(gym_id=2)

    return jsonify({"status": "success", "workouts": result}), 200

