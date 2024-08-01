"""
 data for when API is unavailable/unit testing
 """

import random

class Client:
    """
    Client class
    """
    def __init__(self, periods:list, current_period:object):
        self.current_period = current_period
        self.periods = periods #[trimester1, trimester2, ...]

class Trimester:
    """
    Trimester class
    """
    def __init__(self, name:str, grades:list):
        self.name = name
        self.grades = grades # [grade1, grade2, ...]

class Grade:
    """
    Grade class
    """
    def __init__(self, subject:str, grade:str, out_of:str, is_optionnal:bool,
                 is_bonus:bool, coefficient:str, comment:str, average:str = None):
        self.subject = subject
        self.grade = grade
        self.out_of = out_of
        self.is_optionnal = is_optionnal
        self.is_bonus = is_bonus
        self.coefficient = coefficient
        self.comment = comment
        self.average = average

class Subject:
    """
    Subject class
    """
    def __init__(self, name:str):
        self.name = name

sample_client = Client([
    Trimester("T1", [
        Grade(Subject("Maths"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade1", str(random.randint(5, 20))),
        Grade(Subject("Physique"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade2", str(random.randint(5, 20))),
        Grade(Subject("Francais"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade3", str(random.randint(5, 20))),
        Grade(Subject("SCIENCES VIE & TERRE"), str(random.randint(5, 20)), "20", False, False,
               str(random.randint(1, 6)), "grade4", str(random.randint(5, 20))),
        Grade(Subject("Histoire"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade5", str(random.randint(5, 20))),
        Grade(Subject("Geographie"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade6", str(random.randint(5, 20))),
        Grade(Subject("Anglais"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade7", str(random.randint(5, 20))),
        Grade(Subject("Espagnol"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade8", str(random.randint(5, 20))),
    ]),
    Trimester("T2", [
        Grade(Subject("Maths"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade1", str(random.randint(5, 20))),
        Grade(Subject("Physique"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade2", str(random.randint(5, 20))),
        Grade(Subject("Francais"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade3", str(random.randint(5, 20))),
        Grade(Subject("SCIENCES VIE & TERRE"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade4", str(random.randint(5, 20))),
        Grade(Subject("Histoire"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade5", str(random.randint(5, 20))),
        Grade(Subject("Geographie"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade6", str(random.randint(5, 20))),
        Grade(Subject("Anglais"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade7", str(random.randint(5, 20))),
        Grade(Subject("Espagnol"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade8", str(random.randint(5, 20))), 
    ])
],
    Trimester("T2", [
        Grade(Subject("Maths"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade1", str(random.randint(5, 20))),
        Grade(Subject("Physique"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade2", str(random.randint(5, 20))),
        Grade(Subject("Francais"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade3", str(random.randint(5, 20))),
        Grade(Subject("SCIENCES VIE & TERRE"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade4", str(random.randint(5, 20))),
        Grade(Subject("Histoire"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade5", str(random.randint(5, 20))),
        Grade(Subject("Geographie"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade6", str(random.randint(5, 20))),
        Grade(Subject("Anglais"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade7", str(random.randint(5, 20))),
        Grade(Subject("Espagnol"), str(random.randint(5, 20)), "20", False, False,
              str(random.randint(1, 6)), "grade8", str(random.randint(5, 20))),
    ])
)

def unit_test():
    """
    Unit test for data_test.py
    """
    assert True # placeholder until actual unit tests are implemented
