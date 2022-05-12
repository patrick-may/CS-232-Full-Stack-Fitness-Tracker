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

@lifter_api_blueprint.route('/api/v1/members/', methods=["PUT"])
def update_member():
    update_id = request.json["gym_id"]
    update_member = Gym_Member(request.json["uname"], request.json["uage"], request.json["usex"])

    member_DB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    member_DB.update_member_info(update_id, update_member)

    return jsonify( {"status":"success", "updated member":member_DB.select_individual_member(update_id)} ), 200

@lifter_api_blueprint.route('/api/v1/members/', methods=["DELETE"])
def delete_members():
    memberDB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    
    delete_id = request.json["gym_id"]
    values = memberDB.select_individual_member(delete_id)
    memberDB.delete_member(delete_id)

    return jsonify({"status": "success", "deleted": values}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", methods=["POST"])
def create_weight_set():
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)

    new_set = Weight_Set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"], request.json["reps"], request.json["weight"])
    
    setDB.insert_weight_set(new_set)

    added_set = setDB.select_weight_set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"])
    
    return jsonify({"status":"success", "added":added_set}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", methods=["PUT"])
def update_weight_set():
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)

    update_set = Weight_Set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"], request.json["reps"], request.json["weight"])
    
    setDB.update_weight_set(update_set)

    revised_set = setDB.select_weight_set(update_set.machine_name, update_set.user_id, update_set.timestamp)
    return jsonify({"status":"success", "updated":revised_set}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", methods=["DELETE"])
def delete_weight_set():
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
    
    deleted_set = setDB.select_weight_set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"])
    setDB.delete_weight_set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"])

    
    return jsonify({"status":"success", "deleted":deleted_set}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", defaults={"gym_id":None}, methods=["GET"])
@lifter_api_blueprint.route('/api/v1/weight_sets/<int:gym_id>/', methods=["GET"])
def view_weight_sets(gym_id):
    #if gym_id is none, give all exercises
    if gym_id == None:
        setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)

        values = setDB.select_all_exercises()
        return jsonify({"status":"success", "weight_sets":values}), 200
    else:
        setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
        values = setDB.select_user_exercises(gym_id)
        return jsonify({"status":"success", "weight_sets":values}), 200

@lifter_api_blueprint.route("/api/v1/workouts/", methods=["POST"])
def add_workout():
    db = WorkoutDB(g.mysql_db, g.mysql_cursor)

    create_id = request.json["gym_id"]
    create_date = request.json["workout_date"]
    create_duration = request.json["duration"]
    create_exercises_dict = request.json["exercises"]
    set_list = []

    for exercise_dicts in create_exercises_dict:
        set_list.append(Weight_Set( exercise_dicts["machine_name"], str(create_id), create_date, str(exercise_dicts["reps"]), str(exercise_dicts["weight"])))

    new_workout = Workout(create_id, create_date, create_duration, set_list)

    db.insert_workout(new_workout)
    result = db.select_workout(create_id, create_date)
    return jsonify( {"status":"success", "inserted":result} ), 200
    
@lifter_api_blueprint.route('/api/v1/workouts/', defaults={"user_id":None}, methods=["GET"])
@lifter_api_blueprint.route('/api/v1/workouts/<int:user_id>/', methods=["GET"])
def read_workouts(user_id):
    workout_DB = WorkoutDB(g.mysql_db, g.mysql_cursor)
    result = None
    if user_id is not None:
        result = workout_DB.select_all_workouts(user_id)

    else:
        result = workout_DB.select_every_workout()
        
    return jsonify({"status": "success", "workouts": result}), 200
    
@lifter_api_blueprint.route('/api/v1/workouts/', methods=["DELETE"])
def delete_workouts():
    workout_DB = WorkoutDB(g.mysql_db, g.mysql_cursor)
    delete_id = request.json["gym_id"]
    delete_date = request.json["workout_date"]

    result = workout_DB.select_workout(delete_id, delete_date)
    workout_DB.delete_workout(delete_id, delete_date)

    return jsonify({"status": "success", "workouts": result}), 200
    


