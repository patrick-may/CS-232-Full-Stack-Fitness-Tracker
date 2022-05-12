"""
lifter_api.py

Handles backend logic and routing to interface to database
Current supports:
    CRUD operations to gym_member
    CRUD operations to weight_set
    CR*D operations to workout (no update function)
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
    Returns a READABLE form of members

    INPUT: 
        /api/v1/members/ with a 'GET' HTTP command
        /api/v1/members/<int id here> with a 'GET' HTTP command
    
    RETURNS: 
        /api/v1/members/ - json of all members information
        /api/v1/members/<int id here>/ - json of information about desired member by id
        both forms also return a success code
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
    """
    Creates a new gym_member in the gym_member database

    INPUT: 
        /api/v1/members/ with a 'POST' HTTP command
            inside json recieved, have valid pairs of "name":<member name>, "age":<member age>, and "sex":<member sex>
    
    RETURNS: 
        json file with notable key pair "user id" paired to the created user's gym_id, success code
        
    """
    new_member = Gym_Member(request.json["name"], request.json["age"], request.json["sex"])

    member_DB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    member_DB.insert_individual_member(new_member)

    return jsonify( {"status":"success", "user_id":new_member.gym_id} ), 200

@lifter_api_blueprint.route('/api/v1/members/', methods=["PUT"])
def update_member():
    """
    Updates a gym_member in the gym_member database by gym_id

    INPUT: 
        /api/v1/members/ with a 'PUT' HTTP command
            inside json recieved, have valid pairs of "gym_id":<update id>, 
                "uname":<updated name>, 
                "uage":<updated age>, 
                "usex":<updated sex>

    
    RETURNS: 
        json file with notable key pair "user id" paired to the created user's gym_id, success code
        
    """
    update_id = request.json["gym_id"]
    update_member = Gym_Member(request.json["uname"], request.json["uage"], request.json["usex"])

    member_DB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    member_DB.update_member_info(update_id, update_member)

    return jsonify( {"status":"success", "updated member":member_DB.select_individual_member(update_id)} ), 200

@lifter_api_blueprint.route('/api/v1/members/', methods=["DELETE"])
def delete_members():
    """
    Deletes a gym_member in the gym_member database by gym_id

    INPUT: 
        /api/v1/members/ with a 'DELETE' HTTP command
            inside json recieved, have valid pairs of "gym_id":<delete id>

    RETURNS: 
        json file with deleted member's information, success code
        
    """
    memberDB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    
    delete_id = request.json["gym_id"]
    values = memberDB.select_individual_member(delete_id)
    memberDB.delete_member(delete_id)

    return jsonify({"status": "success", "deleted": values}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", methods=["POST"])
def create_weight_set():
    """
    Creates a weight_set object and inserts it into our exercise_sets table

    INPUT: 
        /api/v1/weight_sets/ with a 'POST' HTTP command
            inside json recieved, have valid pairs of "machine_name":<new set's machine name>, 
                "gym_id":<user's gym_id>, 
                "exercise_date":<date of doing exercise>, 
                "reps":<# of repetitions>
                "weight":<amount of weight for set>

    RETURNS: 
        json file with notable key pair "added" paired to information on the created weight_set, success code
        
    """
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)

    new_set = Weight_Set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"], request.json["reps"], request.json["weight"])
    setDB.insert_weight_set(new_set)
    added_set = setDB.select_weight_set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"])
    
    return jsonify({"status":"success", "added":added_set}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", methods=["PUT"])
def update_weight_set():
    """
    Updates a weight_set object already in database

    INPUT: 
        /api/v1/weight_sets/ with a 'PUT' HTTP command
            inside json recieved, have valid pairs of "machine_name":<current set's machine name>, 
                "gym_id":<user's gym_id>, 
                "exercise_date":<date of doing exercise>, 
                "reps":<updated number of repetitions>
                "weight":<updated amount of weight>

    RETURNS: 
        json file with notable key pair "updated" paired to information on the updated weight_set, success code
        
    """
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)

    update_set = Weight_Set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"], request.json["reps"], request.json["weight"])
    setDB.update_weight_set(update_set)
    revised_set = setDB.select_weight_set(update_set.machine_name, update_set.user_id, update_set.timestamp)
    
    return jsonify({"status":"success", "updated":revised_set}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", methods=["DELETE"])
def delete_weight_set():
    """
    Deletes a weight_set object from database

    INPUT: 
        /api/v1/weight_sets/ with a 'DELETE' HTTP command
            inside json recieved, have valid pairs of "machine_name":<delete sets machine name>, 
                "gym_id":<user's gym_id>, 
                "exercise_date":<date of doing exercise>, 

    RETURNS: 
        json file with notable key pair "deleted" paired to information on the deleted weight_set, success code
        
    """
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
    
    deleted_set = setDB.select_weight_set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"])
    setDB.delete_weight_set(request.json["machine_name"], request.json["gym_id"], request.json["exercise_date"])

    
    return jsonify({"status":"success", "deleted":deleted_set}), 200

@lifter_api_blueprint.route("/api/v1/weight_sets/", defaults={"gym_id":None}, methods=["GET"])
@lifter_api_blueprint.route('/api/v1/weight_sets/<int:gym_id>/', methods=["GET"])
def view_weight_sets(gym_id):
    """
    Returns Readable weight_set objects

    INPUT: 
        /api/v1/weight_sets/ with a 'GET' HTTP command
        /api/v1/weight_sets/<gym id here>/ with a 'GET' HTTP command

    RETURNS: 
        without a gym_id provided, will return a json object with notable key pair "weight_sets" to a list of all weight_sets
        with gym_id provided, "weight_sets" is paired to all weight sets done by <gym_id>
        both return a success code
        
    """
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
    """
    Creates a workout object and inserts it into our database. Inserts all exercises within the workout into database as well

    INPUT: 
        /api/v1/workouts/ with a 'POST' HTTP command
            inside json recieved, have valid pairs of "gym_id":<user's gym_id>, 
                "workout_date":<date of workout>, 
                "duration":<duration of workout in minutes>, 
                "exercises":<list of individual exercise sets>
                    Each exercise has 3 values:
                        "machine_name":<name of machine used>
                        "reps":<number of reps>
                        "weight":<amount of weight in that set>

    RETURNS: 
        json file with notable key pair "inserted" paired to information on the created workout, success code
        
    """
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
    """
    Returns readable json information on workouts in database

    INPUT: 
        /api/v1/workouts/ with a 'GET' HTTP command
        /api/v1/workouts/<gym id here>/

    RETURNS: 
        json file with notable key pair "added" paired to desired workout information, success code
            * if no gym_id is provided, returns all workouts in database
            * if gym_id is provided, returns all workouts done by user with id gym_id
        
    """
    workout_DB = WorkoutDB(g.mysql_db, g.mysql_cursor)
    result = None
    if user_id is not None:
        result = workout_DB.select_all_workouts(user_id)

    else:
        result = workout_DB.select_every_workout()
        
    return jsonify({"status": "success", "workouts": result}), 200
    
@lifter_api_blueprint.route('/api/v1/workouts/', methods=["DELETE"])
def delete_workouts():
    """
    Deletes a workout from database

    INPUT: 
        /api/v1/workouts/ with a 'DELETE' HTTP command
            inside json recieved, have valid pairs of "gym_id":<user's gym_id>, 
                "workout_date":<date of workout to delete>

    RETURNS: 
        json file with notable key pair "workouts" paired to information on deleted workout, success code
        
    """
    workout_DB = WorkoutDB(g.mysql_db, g.mysql_cursor)
    delete_id = request.json["gym_id"]
    delete_date = request.json["workout_date"]

    result = workout_DB.select_workout(delete_id, delete_date)
    workout_DB.delete_workout(delete_id, delete_date)

    return jsonify({"status": "success", "workouts": result}), 200
    


