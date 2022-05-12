"""
gym_member.py

Includes:
    Gym_Member class, a primarily POD class for members of gym
    Gym_Member_DB class, which interfaces to gym_members database table"""

from datetime import datetime

class Gym_Member:
    def __init__(self, name, age, sex, gym_id=None):
        self._name = name
        self._id = gym_id
        self._age = age
        self._sex = sex

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name
    
    @property
    def gym_id(self):
        return self._id

    @gym_id.setter
    def gym_id(self, new_id):
        self._id = new_id

    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, new_age):
        self._age = new_age

    @property
    def sex(self):
        return self._sex
    
    @sex.setter
    def sex(self, new_sex):
        self._sex = new_sex


class Gym_Member_DB:
    """
    Gym_Member_DB
        Interfaces to gym_members table in database

    Currently supports:
        Create - insert_individual_member(gym_member)
        Read - select_all_members()
                select_individual_member(member_id)
        Update - update_member_info(member_id, updated_member)
        Delete - delete_member(member_id)
    """

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    #Create
    def insert_individual_member(self, gym_member):
        """
        Inserts a gym_member into gym_members table

        ARGS:
            self - python syntax
            gym_member - a Gym_Member object

        RETURNS:
            Nothing
        """

        insert_query = """
            INSERT INTO gym_members (name, age, sex, creation_datetime)
            VALUES (%s, %s, %s, %s);
        """
    
        self._cursor.execute(insert_query, (gym_member.name, gym_member.age, gym_member.sex, datetime.now()))
        self._cursor.execute("SELECT LAST_INSERT_ID() gym_id")
        mem_gym_id = self._cursor.fetchone()
        gym_member.gym_id = mem_gym_id
        self._db_conn.commit()

    #Read All
    def select_all_members(self):
        """
        Selects all gym_members from gym_members table

        ARGS:
            self - python syntax

        RETURNS:
            List of information on all members in gym_members table
        """

        full_query = """
            SELECT * FROM gym_members;
        """
        self._cursor.execute(full_query)
        return self._cursor.fetchall()
        
    #Read
    def select_individual_member(self, member_id):
        """
        Selects a gym_member from gym_members table by specific gym_id

        ARGS:
            self - python syntax
            member_id - a user's gym_id

        RETURNS:
            List of information with one dictionary entry of desired member's information
        """

        individual_select_query = """
            SELECT * FROM gym_members WHERE gym_id=%s;
        """
        self._cursor.execute(individual_select_query, (member_id,))
        return self._cursor.fetchall()

    #Update
    def update_member_info(self, member_id, updated_member):
        """
        Updates an exisiting gym_member by member_id

        ARGS:
            self - python syntax
            member_id - a members' id
            updated_member - a Gym_Member object with correct information

        RETURNS:
            Commits update to database. Returns nothing.
        """

        update_query = """
            UPDATE gym_members
            SET name=%s, age=%s, sex=%s
            WHERE gym_id=%s;
        """
        self._cursor.execute(update_query, (updated_member.name, updated_member.age, updated_member.sex, member_id))
        self._db_conn.commit()

    #Delete
    def delete_member(self, member_id):
        """
        Deletes a gym_member from gym_members table

        ARGS:
            self - python syntax
            member_id - a members' id

        RETURNS:
            Commits delete to database. Returns nothing.
        """
        
        delete_query = """
            DELETE FROM gym_members
            WHERE gym_id=%s;
        """

        self._cursor.execute(delete_query, (member_id,))
        self._db_conn.commit()