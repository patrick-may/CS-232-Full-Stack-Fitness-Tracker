from app.models.workout import Workout, WorkoutDB
from app.models.weight_set import Weight_Set

test_workout = Workout(10, "05/10/2022", 65, 
                [Weight_Set("Pull Up Bar", 10, "05/10/2022", 10, 25),
                Weight_Set("Squat", 10, "05/10/2022", 10, 135),
                Weight_Set("Push Up", 10, "05/10/2022", 35, 0)]
    )

def test_workout_create(db_test_client):
    conn, cursor = db_test_client
    db = WorkoutDB(conn, cursor)

    db.insert_workout(test_workout)
    insert_check = db.select_workout(10, "05/10/2022")
    print(insert_check)
    assert(insert_check == test_workout)
    