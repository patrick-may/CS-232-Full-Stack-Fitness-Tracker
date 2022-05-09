"""
Data class for what a workout object will be

Current design is a little bit tricky, as the actual exercises are
Stored in another table. Current idea is to timestamp whenever an exercise is done
And then identify exercises of that workout if they are within workout begin and workout ending

"""
from xxlimited import new


class Workout:
    def __init__(self, gym_id, date_time, duration, weight_sets):
        self._gym_id = gym_id
        self._date_time = date_time
        self._duration = duration
        self._weight_sets = weight_sets
    
    @property
    def month(self):
        return self._month

    @property
    def timestamp(self):
        return self._date_time

    @timestamp.setter
    def date(self, new_date):
        self._date_time = new_date

    @property
    def excercises(self):
        return self._excercises
    
    @excercises.setter
    def excercises(self, replacement_ex_list):
        self._excercises = replacement_ex_list
    
    def add_excercise(self, new_ex):
        self._excercises.append(new_ex)

class WorkoutDB:
    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    #Create
    def insert_workout(self, new_workout):
        insert_workout_query = """
            INSERT INTO workouts (gym_id, date_time, duration)
            VALUES (%s, %s, %s);
        """
        workout_tuple = (new_workout.gym_id, new_workout.timestamp, new_workout.duration)
        self._cursor.execute(insert_workout_query, workout_tuple)

        for weight_set in new_workout.exercises:
            insert_exercise_query = """
                INSERT INTO exercise_sets (machine_name, gym_id, date_time, reps, weight)
                VALUES (%s, %s, %s, %s, %s);
            """

            exercise_tuple = (weight_set.name, weight_set.gym_id, 
                        weight_set.timestamp, weight_set.reps, weight_set.weight)

            self._cursor.execute(insert_exercise_query, exercise_tuple)
        
        self._db_conn.commit()
    
    #Read
    def select_workout(self, gym_id, date):
        select_query = """
            SELECT * from workouts
            WHERE gym_id=%s, date_time=%s;
        """
        self._cursor.execute(select_query, (gym_id, date))
        
        from weight_set import Weight_Set_DB
        exercisesDB = Weight_Set_DB(self._db_conn, self._cursor)
        exercisesDB.select_workout_exercises(gym_id, date)
        return self._cursor.fetchall()

    def update_workout(self, old_workout, new_workout):
        from weight_set import Weight_Set_DB
        exercisesDB = Weight_Set_DB(self._db_conn, self._cursor)

        if old_workout.gym_id == new_workout.gym_id and old_workout.timestamp == new_workout.timestamp:
            #then it is the "same" workout, just just update the exercises.
            for machine, user_id, timestamp, x, y in old_workout.exercises:
                exercisesDB.delete_weight_set(machine,user_id, timestamp)

            for machine, user_id, timestamp, x, y in new_workout.exercises:
                exercisesDB.insert_weight_set(machine,user_id, timestamp)
        
        else:
            self.delete_workout(old_workout)
            self.insert_workout(new_workout)

    def delete_workout(self, gym_id, date):
        delete_query = """
        DELETE from workouts
        WHERE gym_id=%s, date_time=%s;
        """
        self._cursor.execute(delete_query, (gym_id, date))

        sets_delete_query = """
        DELETE from exercise_sets
        WHERE gym_id=%s, date=%s;
        """
        self._cursor.execute(sets_delete_query, (gym_id, date))
        self._db_conn.commit()

    
            
