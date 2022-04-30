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

    @id.setter
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