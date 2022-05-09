import pytest
from datetime import datetime

from app.models.gym_member import Gym_Member

def test_constructor():
    name = "Jimothy"
    gym_mem = Gym_Member(name, 99, 'M')
    assert gym_mem.age == 99
    assert gym_mem.name == "Jimothy"
    assert gym_mem.sex == 'M'

def test_setters():
    gym_mem = Gym_Member("Jimothy", 99, "M")
    gym_mem.name = "New Name"
    assert gym_mem.name == "New Name"
    gym_mem.gym_id = 5
    assert gym_mem.gym_id == 5
    gym_mem.age = 45
    assert gym_mem.age == 45
    gym_mem.sex = "F"
    assert gym_mem.sex == "F"