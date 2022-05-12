import json

def test_insert_set(flask_test_client):
    json_set = {"gym_id":1, "machine_name":"Squat Rack 2", "exercise_date":"05/12/2022", "reps":5, "weight":225}

    request = flask_test_client.post("/api/v1/weight_sets/", json=json_set)

    assert request.status_code == 200

    data = json.loads(request.data.decode())

    # data returned from POST has two values, "status" and "added". "added" will have attributes
    # of weight set that was just added to DB
    assert data["status"] == "success"
    assert data["added"][0]["gym_id"] == 1
    assert data["added"][0]["machine_name"] == "Squat Rack 2"
    assert data["added"][0]["exercise_date"] == "05/12/2022"
    assert data["added"][0]["reps"] == 5
    assert data["added"][0]["weight"] == 225

def test_update_set(flask_test_client):
    #update sets and reps 
    json_set_update = {"gym_id":1, "machine_name":"Squat Rack 2", "exercise_date":"05/12/2022", "reps":10, "weight":15}

    request = flask_test_client.put("/api/v1/weight_sets/", json=json_set_update)

    assert request.status_code == 200
    
    #returned data has an "updated" key that links to data of the updated weight set
    data = json.loads(request.data.decode())
    assert data["status"] == "success"
    # check that the updated data has been changed
    assert data["updated"][0]["reps"] == 10
    assert data["updated"][0]["weight"] == 15

def test_delete_set(flask_test_client):
    json_delete = {"gym_id":1, "machine_name":"Squat Rack 2", "exercise_date":"05/12/2022"}

    request = flask_test_client.delete("/api/v1/weight_sets/", json=json_delete)

    assert request.status_code == 200

    #after deletion there should be no exercises in DB
    request = flask_test_client.get("/api/v1/weight_sets/")
    data = json.loads(request.data.decode())

    assert data["status"] == "success"
    # length should be 0, not 0 => true
    assert not len(data["weight_sets"])

def test_views(flask_test_client):
    new_set_1 = {"gym_id":1, "machine_name":"Pull Up Bar", "exercise_date":"05/12/2022", "reps":7, "weight":25}
    new_set_2 = {"gym_id":3, "machine_name":"Squat Rack 2", "exercise_date":"05/13/2022", "reps":5, "weight":225}

    flask_test_client.post("/api/v1/weight_sets/", json=new_set_1)
    flask_test_client.post("/api/v1/weight_sets/", json=new_set_2)

    all_request = flask_test_client.get("/api/v1/weight_sets/")
    individual_request = flask_test_client.get("/api/v1/weight_sets/3/")

    assert all_request.status_code == 200
    assert individual_request.status_code == 200
    all_data = json.loads(all_request.data.decode())
    individual_data =json.loads(individual_request.data.decode())
    assert len(all_data["weight_sets"]) == 2
    assert len(individual_data["weight_sets"]) == 1
    assert individual_data["weight_sets"][0]["machine_name"] == "Squat Rack 2"
    assert individual_data["weight_sets"][0]["gym_id"] == 3

