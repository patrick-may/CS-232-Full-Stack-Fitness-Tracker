"""
weight_set.py

Includes:
    Weight_Set - primarily a POD class for individual weight sets
    Weight_Set_DB - class that interfaces weight sets to database
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
        return self._machine_name
    
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
    """
    Weight_Set_DB
        Interfaces to exercise_sets table in database

    Currently supports:
        Create - insert_weight_set(self, new_weight_set)
        Read - select_user_exercises(self, user_id),
                select_workout_exercises(self, user_id, date),
                select_all_exercises(self),
                select_weight_set(self, machine_name, user_id, timestamp)

        Update - update_weight_set(self, update_set)
        Delete - delete_weight_set(self, machine_name, user_id, timestamp)
    """

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    #Create
    def insert_weight_set(self, new_weight_set):
        """
        Inserts a weight_set into database

        ARGS:
            self - python syntax
            new_weight_set - Weight_Set object to insert

        RETURNS:
            Nothing
        """

        insert_query = """
            INSERT INTO exercise_sets (machine_name, gym_id, exercise_date, reps, weight)
            VALUES (%s, %s, %s, %s, %s)
        """

        insert_values = (new_weight_set.machine_name, new_weight_set.user_id, 
                        new_weight_set.timestamp, new_weight_set.reps, new_weight_set.weight)

        self._cursor.execute(insert_query, insert_values)
        self._db_conn.commit()
        
    #Read all exercises for one user
    def select_user_exercises(self, user_id):
        """
        Reads all exercises of a specific user

        ARGS:
            self - python syntax
            user_id - specific user that desires their weight_sets

        RETURNS:
            List of weight sets done by user
        """

        select_query = """
            SELECT * FROM exercise_sets WHERE gym_id=%s;
        """
        select_tuple = (user_id,)
        self._cursor.execute(select_query, select_tuple)
        return self._cursor.fetchall()

    #Read all from a workout
    def select_workout_exercises(self, user_id, date):
        """
        Reads all exercises of a specific user at specific date

        ARGS:
            self - python syntax
            user_id - specific user that desires their weight_sets
            date - day of exercises wanting to be extracted

        RETURNS:
            List of weight sets done by user on specific date
        """

        select_query = """
            SELECT * FROM exercise_sets WHERE gym_id=%s AND exercise_date=%s;
        """
        select_tuple = (user_id, date)
        self._cursor.execute(select_query, select_tuple)
        return self._cursor.fetchall()

    #Read all from DB
    def select_all_exercises(self):
        """
        Reads all exercises in database

        ARGS:
            self - python syntax

        RETURNS:
            List of all weight sets done
        """

        full_select_query = """
            SELECT * FROM exercise_sets;
        """
        self._cursor.execute(full_select_query)
        return self._cursor.fetchall()
        
    #Read
    def select_weight_set(self, machine_name, user_id, timestamp):
        """
        Reads a specific weight_set from database

        ARGS:
            self - python syntax
            machine_name - name of machine used in specific weight set
            user_id - specific user that desires their weight_sets
            timestamp - date of specific set done
        
        RETURNS:
            List of 1 entry: desired weight_set
        """

        select_query = """
            SELECT * FROM exercise_sets WHERE machine_name=%s AND gym_id=%s AND exercise_date=%s;
        """
        select_tuple = (machine_name, user_id, timestamp)

        self._cursor.execute(select_query, select_tuple)
        return self._cursor.fetchall()

    #Update
    def update_weight_set(self, update_set):
        """
        Updates a specific set's reps and weight

        ARGS:
            self - python syntax
            update_set - Weight_Set object with updated fields

        RETURNS:
            Commits update to database. Returns nothing.
        """

        update_query = """
            UPDATE exercise_sets
            SET reps=%s, weight=%s
            WHERE machine_name=%s AND gym_id=%s AND exercise_date=%s;
        """

        update_tuple = (update_set.reps, update_set.weight,
                        update_set.machine_name, update_set.user_id,
                        update_set.timestamp)
        
        self._cursor.execute(update_query, update_tuple)
        self._db_conn.commit()

    #Delete
    def delete_weight_set(self, machine_name, user_id, timestamp):
        """
        Deletes a specific weight set

        ARGS:
            self - python syntax
            machine_name - name of machine used in specific set
            user_id - specific user that desires their weight_sets
            timestamp - date of specific sets

        RETURNS:
            List of weight sets done by user
        """

        delete_query = """
            DELETE FROM exercise_sets
            WHERE machine_name=%s AND gym_id=%s AND exercise_date=%s;
        """

        delete_tuple = (machine_name, user_id, timestamp)

        self._cursor.execute(delete_query, delete_tuple)
        self._db_conn.commit()
