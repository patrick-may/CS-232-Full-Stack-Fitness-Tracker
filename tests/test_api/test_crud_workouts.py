import json


def test_insert_workout(flask_test_client):
    """
    GIVEN an API insert call
    WHEN a workout is inserted in the database
    THEN check if workout is in the database and API return is correct
    """
    # workouts are linked to users, so first we create a user to give
    # the workout to
    request = flask_test_client.post(
        "/api/v1/members/", json={"name": "Timothy", "age": 19, "sex": "M"})

    data = json.loads(request.data.decode())
    timothy_id = data["user_id"]["gym_id"]

    workout_json = {"gym_id": timothy_id, "workout_date": "05/24/2022", "duration": 48,
                    "exercises": [{"machine_name": "Squat Rack 1", "reps": 5, "weight": 135},
                                  {"machine_name": "Pull Up Bar 2",
                                      "reps": 13, "weight": 0},
                                  {"machine_name": "Flat Bench 1", "reps": 8, "weight": 10}]}

    request = flask_test_client.post("/api/v1/workouts/", json=workout_json)

    data = json.loads(request.data.decode())
    assert request.status_code == 200
    assert data["status"] == "success"
    assert data["inserted"][0]["gym_id"] == timothy_id
    assert data["inserted"][0]["workout_date"] == "05/24/2022"


def test_delete_workout(flask_test_client):
    """
    GIVEN an API delete call
    WHEN a workout is deleted in the database
    THEN check if workout is in the database and API return is correct
    """
    # workouts are linked to users, so first we create a user to give
    # the workout to

    old_values = json.loads(flask_test_client.get(
        "/api/v1/workouts/").data.decode())

    assert old_values["status"] == "success"
    assert len(old_values["workouts"])

    delete_json = {"gym_id": 1, "workout_date": "05/24/2022"}
    request = flask_test_client.delete("/api/v1/workouts/", json=delete_json)

    new_values = json.loads(flask_test_client.get(
        "/api/v1/workouts/").data.decode())

    assert new_values["status"] == "success"
    assert len(new_values["workouts"]) == 0


def test_view_workout(flask_test_client):
    """
    GIVEN an API view call
    WHEN a workout is in the database
    THEN check if workout is returned correctly from the database and API return is correct
    """
    # insert another member to test whole view and individual member view
    request = flask_test_client.post(
        "/api/v1/members/", json={"name": "Second Member", "age": 49, "sex": "F"})

    assert request.status_code == 200
    workout_json_1 = {"gym_id": 1, "workout_date": "05/24/2022", "duration": 48,
                      "exercises": [{"machine_name": "Squat Rack 1", "reps": 5, "weight": 135},
                                    {"machine_name": "Pull Up Bar 2",
                                        "reps": 13, "weight": 0},
                                    {"machine_name": "Flat Bench 1", "reps": 8, "weight": 10}]}

    request = flask_test_client.post("/api/v1/workouts/", json=workout_json_1)
    assert request.status_code == 200
    workout_json_2 = {"gym_id": 2, "workout_date": "05/24/2022", "duration": 35,
                      "exercises": [{"machine_name": "Squat Rack 3", "reps": 9, "weight": 135},
                                    {"machine_name": "Decline Bench 2",
                                     "reps": 14, "weight": 40},
                                    {"machine_name": "Deadlift Platform 1", "reps": 5, "weight": 225}]}

    request = flask_test_client.post("/api/v1/workouts/", json=workout_json_2)
    assert request.status_code == 200

    request = flask_test_client.get("/api/v1/workouts/")
    assert request.status_code == 200
    data = json.loads(request.data.decode())
    assert data["status"] == "success"
    assert len(data["workouts"]) == 2

    request = flask_test_client.get("/api/v1/workouts/2/")
    assert request.status_code == 200
    data = json.loads(request.data.decode())
    assert data["status"] == "success"
    assert len(data["workouts"]) == 1
    assert data["workouts"][0]["gym_id"] == 2
    assert data["workouts"][0]["duration"] == 35
