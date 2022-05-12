from app.models.workout import Workout, WorkoutDB
from app.models.gym_member import Gym_Member, Gym_Member_DB
from app.models.weight_set import Weight_Set

exercise_list = [Weight_Set("Pull Up Bar", 1, "05/10/2022", 10, 25),
                 Weight_Set("Squat", 1, "05/10/2022", 10, 135),
                 Weight_Set("Push Up", 1, "05/10/2022", 35, 0)]

test_workout = Workout(1, "05/10/2022", 65, exercise_list)


def test_workout_create(db_test_client):
    """
    GIVEN a Gym_Member_DB
    WHEN a new workout is inserted
    THEN check if workout is in the database
    """
    conn, cursor = db_test_client

    new_member = Gym_Member("Jimothy", 99, 'M')
    db = Gym_Member_DB(conn, cursor)
    db.insert_individual_member(new_member)

    db = WorkoutDB(conn, cursor)

    db.insert_workout(test_workout)
    insert_check = db.select_workout(1, "05/10/2022")[0]
    assert insert_check["gym_id"] == 1
    assert insert_check["workout_date"] == "05/10/2022"
    assert insert_check["duration"] == 65
    assert len(insert_check["exercises"]) == 3

    conn.commit()


def test_workout_delete(db_test_client):
    """
    GIVEN a Gym_Member_DB
    WHEN a workout is deleted
    THEN check if workout is in the database
    """

    conn, cursor = db_test_client

    new_member = Gym_Member("Jimothy", 99, 'M')
    db = Gym_Member_DB(conn, cursor)

    db = WorkoutDB(conn, cursor)

    # check if in
    assert len(db.select_workout(1, "05/10/2022")) == 1

    # delete
    db.delete_workout(1, "05/10/2022")

    # check if not it
    assert len(db.select_workout(1, "05/10/2022")) == 0
    conn.commit()


def test_workout_update(db_test_client):
    """
    GIVEN a Gym_Member_DB
    WHEN a workout is updated
    THEN check if workout is updated 
    """
    conn, cursor = db_test_client

    new_member = Gym_Member("Jimothy", 99, 'M')
    db = Gym_Member_DB(conn, cursor)
    db.insert_individual_member(new_member)

    db = WorkoutDB(conn, cursor)
    db.insert_workout(test_workout)

    updated_workout = Workout(
        1, "05/25/2022", 45, [Weight_Set("Pull Up", 10, "05/25/2022", 100, -40)])
    db.update_workout(test_workout, updated_workout)
    assert len(db.select_workout(1, "05/10/2022")) == 0
    assert len(db.select_workout(1, "05/25/2022")) == 1
    conn.commit()
