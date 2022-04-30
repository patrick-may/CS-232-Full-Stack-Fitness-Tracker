"""
Data class for what a workout object will be
"""
class Workout:
    def __init__(self, gym_id, date, duration, excercises):
        self._gym_id = gym_id
        #date should be recieved in 
        date_info = date.split("/")
        self._month = date_info[0]
        self._day = date_info[1]
        self._year = date_info[2]
        self._duration = duration

        #excercises should be a list of machines used. 
        #proper overloading support coming soon
        self._excercises = excercises
    
    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, new_month):
        self._month = new_month

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, new_day):
        self._day = new_day

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, new_year):
        self._year = new_year

    @property
    def excercises(self):
        return self._excercises
    
    @excercises.setter
    def excercises(self, replacement_ex_list):
        self._excercises = replacement_ex_list
    
    def add_excercise(self, new_ex):
        self._excercises.append(new_ex)