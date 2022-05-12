from app.models.weight_set import Weight_Set, Weight_Set_DB
from app.models.workout import Workout, WorkoutDB


def test_create(db_test_client):
    """
    GIVEN a Weight_Set_DB
    WHEN a new weight set is inserted
    THEN check if weight set is in the database
    """

    conn, cursor = db_test_client
    #cursor.execute("ALTER TABLE exercise_sets NOCHECK CONSTRAINT ALL")

    db = Weight_Set_DB(conn, cursor)

    old_size = len(db.select_all_exercises())
    new_set = Weight_Set("Squat Machine 1", 1, "05/08/2022", 8, 135)
    db.insert_weight_set(new_set)
    new_size = len(db.select_all_exercises())
    assert old_size + 1 == new_size

    conn.commit()


def test_unique_select(db_test_client):
    """
    GIVEN a Weight_Set_DB
    WHEN a weight set is inserted
    THEN check if a specific weight set can be extracted for viewing
    """
    conn, cursor = db_test_client
    db = Weight_Set_DB(conn, cursor)

    special_set = Weight_Set("Muscle Up Bar", 1, "05/08/2022", 6, 0)
    db.insert_weight_set(special_set)
    pulled_set = db.select_weight_set("Muscle Up Bar", 1, "05/08/2022")[0]

    assert pulled_set["reps"] == 6
    assert pulled_set["weight"] == 0

    conn.commit()


def test_individual_update(db_test_client):
    """
    GIVEN a Weight_Set_DB
    WHEN a weight set is updated
    THEN check if individual weight set is updated
    """
    conn, cursor = db_test_client
    db = Weight_Set_DB(conn, cursor)

    special_set = Weight_Set("Muscle Up Bar", 1, "05/08/2022", 6, 0)
    special_set.reps = 100
    special_set.weight = 10
    db.update_weight_set(special_set)
    pulled_set = db.select_weight_set("Muscle Up Bar", 1, "05/08/2022")[0]

    assert pulled_set["reps"] == 100
    assert pulled_set["weight"] == 10

    conn.commit()


def test_delete(db_test_client):
    """
    GIVEN a Weight_Set_DB
    WHEN a new weight set is deleted
    THEN check if weight set is in the database
    """
    conn, cursor = db_test_client
    db = Weight_Set_DB(conn, cursor)

    special_set = Weight_Set("Muscle Up Bar", 1, "05/08/2022", 6, 0)
    db.insert_weight_set(special_set)

    sets = db.select_all_exercises()
    for weight_sets in sets:

        db.delete_weight_set(
            weight_sets["machine_name"], weight_sets["gym_id"], weight_sets["exercise_date"])

    assert len(db.select_all_exercises()) == 0
    conn.commit()


def test_weightset_workout_pull(db_test_client):
    """
    GIVEN a Weight_Set_DB
    WHEN a weight set is inserted
    THEN check if all weight sets of a user are in the database
    """
    conn, cursor = db_test_client
    db = Weight_Set_DB(conn, cursor)

    exercises = [Weight_Set("Pull Up Bar", 1, "05/08/2022", 10, 25),
                 Weight_Set("Squat", 1, "05/08/2022", 10, 135),
                 Weight_Set("Push Up", 1, "05/08/2022", 35, 0)]

    for ex in exercises:
        db.insert_weight_set(ex)

    workout_list = db.select_workout_exercises(1, "05/08/2022")

    assert len(workout_list) == 3
    assert workout_list[0]["machine_name"] == "Pull Up Bar"
    assert workout_list[0]["gym_id"] == 1
    assert workout_list[0]["exercise_date"] == "05/08/2022"
    assert workout_list[0]["reps"] == 10
    assert workout_list[0]["weight"] == 25
