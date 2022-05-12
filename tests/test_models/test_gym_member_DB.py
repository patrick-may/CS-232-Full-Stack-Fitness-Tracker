from app.models.gym_member import Gym_Member, Gym_Member_DB


def test_member_insert(db_test_client):
    """
    GIVEN a Gym_Member_DB
    WHEN a new gym member is inserted
    THEN check if the gym member is in the database
    """
    conn, cursor = db_test_client
    db = Gym_Member_DB(conn, cursor)

    new_member = Gym_Member("Jimothy", 99, 'M')
    db.insert_individual_member(new_member)

    id_val = new_member.gym_id
    found_mem = db.select_individual_member(id_val["gym_id"])
    assert found_mem[0]['name'] == "Jimothy"

    conn.commit()


def test_member_delete(db_test_client):
    """
    GIVEN a Gym_Member_DB
    WHEN a gym member is deleted
    THEN check if the gym member is in the database
    """
    conn, cursor = db_test_client
    db = Gym_Member_DB(conn, cursor)

    new_member = Gym_Member("Jimothy", 99, 'M')
    db.insert_individual_member(new_member)

    members = db.select_all_members()
    for mem in members:
        db.delete_member(mem["gym_id"])

    assert len(db.select_all_members()) == 0

    conn.commit()


def test_member_update(db_test_client):
    """
    GIVEN a Gym_Member_DB
    WHEN a gym member is update
    THEN check using read function if updates occur
    """
    conn, cursor = db_test_client
    db = Gym_Member_DB(conn, cursor)

    new_member = Gym_Member("Jimothy", 99, 'M')
    db.insert_individual_member(new_member)
    id_val = new_member.gym_id["gym_id"]

    replace_member = Gym_Member("FizzBuzz", 78, "F")
    db.update_member_info(id_val, replace_member)
    updated = db.select_individual_member(id_val)[0]
    assert updated["name"] == "FizzBuzz"
    assert updated["age"] == 78
    assert updated["sex"] == "F"

    conn.commit()
