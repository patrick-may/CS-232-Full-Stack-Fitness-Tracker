import json

def test_mem_insert(flask_test_client):

    #old_member_list_len = len(flask_test_client.get("/api/v1/members"))

    request = flask_test_client.post("/api/v1/members/", json={"name":"Jimothy", "age":19, "sex":"M"})

    assert request.status_code == 200

    data = json.loads(request.data.decode())

    assert data["user_id"]["gym_id"] == 1
    assert data["status"] == "success"

    request = flask_test_client.post("/api/v1/members/", json={"name":"tester 2", "age":99, "sex":"F"})

    assert request.status_code == 200
    
    data = json.loads(request.data.decode())

    assert data["user_id"]["gym_id"] == 2
    assert data["status"] == "success"

#def test_workout_insert(flask_test_client):

#    insert_workout_json = {"gym_id" : 1,
#    "workout_date":"05/10/2020", "duration": 65,
#    "exercises": [{"gym_id":1, "machine_name":"Squat Rack 1", "exercise_date":"05/10/2022", "reps":5, "weight":135}]}

#    request = flask_test_client.post("/api/v1/1/workouts/", json=insert_workout_json)

#    assert request.status_code == 200


#def test_mem_delete(flask_test_client):

#    request = flask_test_client.delete("/api/v1/members/")

#    assert request.status_code == 200

#    data = json.loads(request.date.decode())

#    assert data["deleted"][0]["name"] == "Jimothy"
