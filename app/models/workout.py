"""
workout.py

Includes:
    Workout - primarily a POD class for workouts, which have gym_id, date, duration, and list of weight sets
    WorkoutDB - class that interfaces Workout to database
"""
from models.weight_set import Weight_Set, Weight_Set_DB

class Workout:
    def __init__(self, gym_id, date_time, duration, weight_sets):
        self._gym_id = gym_id
        self._date_time = date_time
        self._duration = duration
        self._weight_sets = weight_sets
    
    @property 
    def user_id(self):
        return self._gym_id

    @user_id.setter
    def user_id(self, new_id):
        self._gym_id = new_id

    @property
    def duration(self):
        return self._duration

    @property
    def timestamp(self):
        return self._date_time

    @timestamp.setter
    def date(self, new_date):
        self._date_time = new_date

    @property
    def exercises(self):
        return self._weight_sets
    
    @exercises.setter
    def exercises(self, replacement_ex_list):
        self._weight_sets = replacement_ex_list
    
    def add_excercise(self, new_ex):
        self._weight_sets.append(new_ex)

class WorkoutDB:
    """
    WorkoutDB
        Interfaces to workouts table in database

    Currently supports:
        Create - insert_workout(self, new_workout)
        Read - select_workout(self, gym_id, date),
               select_all_workouts(self, gym_id),
               select_every_workout(self)
        Update - update_workout(self, old_workout, new_workout)
        Delete - delete_workout(self, gym_id, date)
    """

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    #Create
    def insert_workout(self, new_workout):
        """
        Inserts a workout into database, which includes all exercises that go along with the workout

        ARGS:
            self - python syntax
            new_workout - Workout object to be inserted

        RETURNS:
            Commits object creation. Returns Nothing.
        """
        
        insert_workout_query = """
            INSERT INTO workouts (gym_id, workout_date, duration)
            VALUES (%s, %s, %s);
        """
        workout_tuple = (new_workout.user_id, new_workout.timestamp, new_workout.duration)
        self._cursor.execute(insert_workout_query, workout_tuple)
        
        for weight_set in new_workout.exercises:
            insert_exercise_query = """
                INSERT INTO exercise_sets (machine_name, gym_id, exercise_date, reps, weight)
                VALUES (%s, %s, %s, %s, %s);
            """

            exercise_tuple = (weight_set.machine_name, weight_set.user_id, 
                        weight_set.timestamp, weight_set.reps, weight_set.weight)
        
            self._cursor.execute(insert_exercise_query, exercise_tuple)
        
        self._db_conn.commit()
    
    #Read
    def select_workout(self, gym_id, date):
        """
        Selects an individual workout by gym_id and date

        ARGS:
            self - python syntax
            gym_id - user's id 
            date - date of specific workout

        RETURNS:
            Information on specific workout
        """

        select_query = """
            SELECT * FROM workouts
            WHERE gym_id=%s AND workout_date=%s;
        """
        self._cursor.execute(select_query, (gym_id, date))
        
       
        exercisesDB = Weight_Set_DB(self._db_conn, self._cursor)
        
        vals = self._cursor.fetchall()
        
        if len(vals): vals[0]["exercises"] = exercisesDB.select_workout_exercises(gym_id, date)
        return vals

    def select_all_workouts(self, gym_id):
        """
        Selects an individual's workouts by gym_id

        ARGS:
            self - python syntax
            gym_id - user's id 
            date - date of specific workout

        RETURNS:
            Information on specific workouts
        """

        select_query = """
            SELECT * FROM workouts
            WHERE gym_id=%s;
        """    

        self._cursor.execute(select_query, (gym_id,))

        vals = self._cursor.fetchall()
        if len(vals):
            exercisesDB = Weight_Set_DB(self._db_conn, self._cursor)
            for workouts in vals:
                workouts["exercises"] = exercisesDB.select_workout_exercises(gym_id, workouts["workout_date"])

        return vals

    def select_every_workout(self):
        """
        Selects all workouts

        ARGS:
            self - python syntax

        RETURNS:
            List of information on every workout in database
        """

        select_query = """
            SELECT * FROM workouts
        """    

        self._cursor.execute(select_query)

        vals = self._cursor.fetchall()
        
        if len(vals):
            exercisesDB = Weight_Set_DB(self._db_conn, self._cursor)
            for workouts in vals:
                workouts["exercises"] = exercisesDB.select_workout_exercises(workouts["gym_id"], workouts["workout_date"])

        return vals


    def update_workout(self, old_workout, new_workout):
        """
        Updates a workout

        ARGS:
            self - python syntax
            old_workout - Workout object that is being updated
            new_workout - Workout object with relavent updates

        RETURNS:
            Commits update to database. returns nothing.
        """
        from models.weight_set import Weight_Set_DB
        exercisesDB = Weight_Set_DB(self._db_conn, self._cursor)

        if old_workout.user_id == new_workout.user_id and old_workout.timestamp == new_workout.timestamp:
            #then it is the "same" workout, just just update the exercises.
            for machine, user_id, timestamp, x, y in old_workout.exercises:
                exercisesDB.delete_weight_set(machine,user_id, timestamp)

            for machine, user_id, timestamp, x, y in new_workout.exercises:
                exercisesDB.insert_weight_set(machine,user_id, timestamp)
        
        else:
            self.delete_workout(old_workout.user_id, old_workout.timestamp)
            self.insert_workout(new_workout)

    def delete_workout(self, gym_id, date):
        """
        Deletes an individual workout by gym_id and date

        ARGS:
            self - python syntax
            gym_id - user's id 
            date - date of specific workout

        RETURNS:
            Commits delete into database. Returns Nothing.
        """
        
        delete_query = """
        DELETE FROM workouts
        WHERE gym_id=%s AND workout_date=%s;
        """
        self._cursor.execute(delete_query, (gym_id, date))

        sets_delete_query = """
        DELETE FROM exercise_sets
        WHERE gym_id=%s AND exercise_date=%s;
        """
        self._cursor.execute(sets_delete_query, (gym_id, date))
        self._db_conn.commit()

    
            
