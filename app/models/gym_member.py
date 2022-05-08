# Class for modeling what a gym member is, currently POD Class

class Gym_Member:
    def __init__(self, name, gym_id, age, sex):
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

#Gym member information is all stored within gym_members table
class Gym_Member_DB:

    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    #Create
    def insert_individual_member(self, gym_member):
        insert_query = """
            INSERT INTO gym_members (name, age, sex)
            VALUES (%s, %s, %s);
        """
    
        self._cursor.execute(insert_query, (gym_member.name, gym_member.age, gym_member.sex))
        self._cursor.execute("SELECT LAST_INSERT_ID() gym_id")
        task_id = self._cursor.fetchone()
        self._db_conn.commit()

    #Read All
    def select_all_members(self):
        full_query = """
            SELECT * from gym_members;
        """
        self._cursor.execute(full_query)
        return self._cursor.fetchall()
        
    #Read
    def select_individual_member(self, member_id):
        individual_select_query = """
            SELECT * from gym_members WHERE gym_id = %s;
        """
        self._cursor.execute(individual_select_query, (member_id,))
        return self._cursor.fetchall()

    #Update
    def update_member_info(self, member_id, updated_member):
        update_query = """
            UPDATE gym_members
            SET name=%s, age=%s, sex=%s
            WHERE gym_id=%s;
        """
        self._cursor.execute(update_query, (updated_member.name, updated_member.age, updated_member.sex, member_id))
        self._db_conn.commit()

    #Delete
    def delete_member(self, member_id):
        delete_query = """
            DELETE from gym_members
            WHERE gym_id=%s;
        """

        self._cursor.execute(delete_query, (member_id,))
        self._db_conn.commit()