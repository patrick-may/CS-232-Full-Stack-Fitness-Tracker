"""
Data class and CRUD class for a workout set
Each Object will have:
    Primary Key is composed of:
        Machine Name 
        Gym_id of member doing excercise
        Timestamp of doing exercise

    Other values:
        Number of repetitions
        Amount of weight
"""
class Weight_Set:
    def __init__(self, machine_name, gym_id, date_time, reps, weight):
        self._machine_name = machine_name
        self._gym_id = gym_id
        self._date_time = date_time
        self._reps = reps
        self._weight = weight
    
    @property
    def machine_name(self):
        return self._name
    
    @machine_name.setter
    def machine_name(self, new_name):
        self._machine_name = new_name
    
    @property
    def user_id(self):
        return self._gym_id

    @user_id.setter
    def user_id(self, new_id):
        self._gym_id = new_id

    @property
    def timestamp(self):
        return self._date_time

    @timestamp.setter
    def timestamp(self, new_date_time):
        self._date_time = new_date_time

    @property
    def reps(self):
        return self._reps

    @reps.setter
    def reps(self, new_rep_ct):
        self._reps = new_rep_ct

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, new_weight):
        self._weight = new_weight

class Weight_Set_DB:

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    #Create
    def insert_weight_set(self, new_weight_set):
        insert_query = """
            INSERT INTO exercise_sets (machine_name, gym_id, date_time, reps, weight)
            VALUES (%s, %s, %s, %s, %s)
        """

        insert_values = (new_weight_set.name, new_weight_set.gym_id, 
                        new_weight_set.timestamp, new_weight_set.reps, new_weight_set.weight)

        self._cursor.execute(insert_query, insert_values)
        self._db_conn.commit()
    
    #Read all from a workout
    def select_workout_exercises(self, user_id, date):
        select_query = """
            SELECT * from exercise_sets WHERE gym_id=%s, date_time=%s;
        """
        select_tuple = (user_id, date)
        self._cursor.execute(select_query, select_tuple)
        return self._cursor.fetchall()
        
    #Read
    def select_weight_set(self, machine_name, user_id, timestamp):
        select_query = """
            SELECT * from exercise_sets WHERE machine_name=%s, gym_id=%s, date_time=%s;
        """
        select_tuple = (machine_name, user_id, timestamp)

        self._cursor.execute(select_query, select_tuple)
        return self._cursor.fetchall()

    #Update
    def update_weight_set(self, update_set):
        update_query = """
            UPDATE exercise_sets
            SET reps=%s, weight=%s
            WHERE machine_name=%s, gym_id=%s, date_time=%s;
        """

        update_tuple = (update_set.reps, update_set.weight,
                        update_set.machine_name, update_set.gym_id,
                        update_set.timestamp)
        
        self._cursor.execute(update_query, update_tuple)
        self._db_conn.commit()

    #Delete
    def delete_weight_set(self, machine_name, user_id, timestamp):
        delete_query = """
            DELETE from exercise_sets
            WHERE machine_name=%s, gym_id=%s, date_time=%s;
        """

        delete_tuple = (machine_name, user_id, timestamp)

        self._cursor.execute(delete_query, delete_tuple)
        self._db_conn.commit()
