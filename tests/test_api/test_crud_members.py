import json

def test_mem_insert(flask_test_client):
    #testing member create
    request = flask_test_client.post("/api/v1/members/", json={"name":"Jimothy", "age":19, "sex":"M"})

    assert request.status_code == 200

    #data returned is dictionary of values about the created member (relevant is the gym_id, which is assigned at creation)
    data = json.loads(request.data.decode())

    assert data["user_id"]["gym_id"] == 1
    assert data["status"] == "success"

    #can insert another member and it still works
    request = flask_test_client.post("/api/v1/members/", json={"name":"tester 2", "age":99, "sex":"F"})

    assert request.status_code == 200
    
    data = json.loads(request.data.decode())
    #checking gym_id increments correctly
    assert data["user_id"]["gym_id"] == 2
    assert data["status"] == "success"

def test_member_update(flask_test_client):

    json_data = {"gym_id":1, "uname":"Cooler Jimothy", "uage":42, "usex":"F"}

    request = flask_test_client.put("/api/v1/members/", json=json_data)

    assert request.status_code == 200

    data = json.loads(request.data.decode())

    #returned value should be gym_member of updated values, checking that updated name was returned
    assert data["status"] == "success"
    assert data["updated member"][0]["name"] == "Cooler Jimothy"


def test_member_delete(flask_test_client):

    json_data = {"gym_id":1}

    request = flask_test_client.delete("/api/v1/members/", json=json_data)

    assert request.status_code == 200

    data = json.loads(request.data.decode())

    # check success, deleted data should be information about user that was deleted
    assert data["status"] == "success"
    assert data["deleted"][0]["name"] == "Cooler Jimothy"

def test_member_get(flask_test_client):
    
    #first do a general request
    request = flask_test_client.get("/api/v1/members/")

    #make sure it passed legally
    assert request.status_code == 200

    data = json.loads(request.data.decode())
    
    #see if success, and currently there should only be 1 member in db, gym_id 2 from test_insert
    assert data["status"] == "success"
    assert len(data["members"]) == 1

    #add another person, we tested insert already so using it here is okay
    flask_test_client.post("/api/v1/members/", json={"name":"Person 3", "age":45, "sex":"F"})

    request = flask_test_client.get("/api/v1/members/")
    assert request.status_code == 200
    data = json.loads(request.data.decode())
    assert data["status"] == "success"
    assert len(data["members"]) == 2

    # test getting a specific user's member information
    request = flask_test_client.get("/api/v1/members/3/")
    assert request.status_code == 200
    data = json.loads(request.data.decode())
    assert data["status"] == "success"
    assert data["members"][0]["name"] == "Person 3" 
    assert data["members"][0]["age"] == 45
    assert data["members"][0]["sex"] == "F"  
