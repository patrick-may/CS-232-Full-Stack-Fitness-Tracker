"""
Data class for a weight machine
Each instance has:
Name
Dictionary of workout sets: 
    { Gym_ids (users) : individual Sets [ (weight, reps), (weight set2, reps set2)] }

"""
class Weight_Machine:
    def __init__(self, name, sets):
        self._name = name
        self._sets = sets
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def sets(self):
        return self._sets

    @sets.setter
    def sets(self, overwrite_dict):
        self._sets = overwrite_dict

    def add_set(self, user_id, weight, reps):
        self._sets[user_id].append( (weight, reps) )