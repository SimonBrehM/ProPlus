from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# *********************
# TABLES OF THE DATABASE
# *********************

class Averages(db.Model):
    date = db.Column(db.String, primary_key=True) # date when the data was inseted, format : YYYY-MM-DD HH-MM-SS.SSSSSS
    period = db.Column(db.String)
    avg_overall = db.Column(db.String)

class Subjects(db.Model):
    name = db.Column(db.String, primary_key = True)
    avg = db.Column(db.String)

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    actual_grade = db.Column(db.String)
    out_of = db.Column(db.Float)
    coeff = db.Column(db.Float)
    description = db.Column(db.String)
    benefical = db.Column(db.String) # grade > subject_avg
    above_class_avg = db.Column(db.Boolean) # grade > class_avg
    avg_class = db.Column(db.String)
    subject = db.Column(db.String)
    period = db.Column(db.String)

# *********************
# *********************

# *********************
# FIRST TABLE ELEMENTS CREATION AND FILLING FUNCTIONS
# *********************

def create_subjects_db(trim:int):
    """
    Creation of all the subjects avilable in the table Subjects
    CAUTION : it does NOT take into account previous subjects added into the db, use it for the launch of the db or an error will appear relative to the primary key
    """
    subjects_avg = calc_avg_subject(trim)
    for subject in subjects_avg.keys():
        sbj = Subjects(name = subject, avg = subjects_avg[subject])
        db.session.add(sbj)
    db.session.commit()
    # /!\ returns None

def create_averages_db(trim:int):
    """
    Creation of an element in the table Averages coming from the period (trim)
    """
    avg = Averages(date = str(datetime.now()), period = trimestre(trim).name, avg_overall = calc_overall_avg(trim))
    db.session.add(avg)
    db.session.commit()
    # /!\ returns None

def create_grades_db(trim:int):
    """
    Creation of all the grades available in the table Grades coming from the period (trim)
    CAUTION : it does NOT take into account previous grades added into the db, use it for the launch of the db or you'll insert grades multiples times
    """
    all_grades = anal_grades(trim)
    for sbj in all_grades:
        for grd in all_grades[sbj]:
            grade = Grades(actual_grade = grd[0], out_of = grd[1], coeff = grd[2], description = grd[3], benefical = grd[4], above_class_avg = grd[5], avg_class = grd[6], subject = grd[7], period = grd[8])
            db.session.add(grade)
    db.session.commit()
    # /!\ returns None

# *********************
# *********************

# *********************
# COMMIT / ADD ONE ELEMENT FUNCTIONS
# *********************

def commit_averages_db(avg_period:str, avg_avg_overall:float):
    """
    Commits one element to the table Averages coming from its period and the overall average
    """
    avg = Averages(date = str(datetime.now()), period = avg_period, avg_overall = avg_avg_overall)
    db.session.add(avg)
    db.session.commit()
    # /!\ returns None

def commit_subjects_db(sbj_name:str, sbj_avg:float):
    """
    Commits one element to the table Subjects coming from its name (/!\ primary key) and the average in this subject
    """
    subject = Subjects(name = sbj_name, avg = sbj_avg)
    db.session.add(subject)
    db.session.commit()
    # /!\ returns None

def commit_grades_db(grd_actual_grade:float, grd_out_of:float, grd_coeff:float, grd_desc:str, grd_benef:bool, grd_above_class:bool, grd_class_avg:float, grd_sbj:str, grd_period:str):
    """
    Commits one element to the table Grades coming from the actual grade, the out_of, the coefficient, the description, if its benefical for the subjects average, if its above the class average, the class average, the subject and its period
    """
    grade = Grades(actual_grade = grd_actual_grade, out_of = grd_out_of, coeff = grd_coeff, description = grd_desc, benefical = grd_benef, above_class_avg = grd_above_class, avg_class = grd_class_avg, subject = grd_sbj, period = grd_period)
    db.session.add(grade)
    db.session.commit()
    # /!\ returns None

# *********************
# *********************

# *********************
# EXTRACTION FUNCTIONS
# *********************

def extract_all_averages_db():
    """Extracts EVERY element from the table Averages and returns it on the form of a list"""
    all_avg = Averages.query.all()
    avg_list = []
    for avg in all_avg:
        avg_list.append([avg.date, avg.period, avg.avg_overall])
    return avg_list
    # type : list

def extract_all_subjects_db():
    """Extracts EVERY element from the table Subjects and returns it on the form of a list"""
    all_sbj = Subjects.query.all()
    sbj_list = []
    for sbj in all_sbj:
        sbj_list.append([sbj.name, sbj.avg])
    return sbj_list
    # type : list

def extract_all_grades_db():
    """Extracts EVERY element from the table Grades and returns it on the form of a list"""
    all_grd = Grades.query.all()
    grd_list = {}
    for grd in all_grd:
        if grd.subject in grd_list:
            grd_list[grd.subject] += [[grd.actual_grade, grd.out_of, grd.coeff, grd.description, grd.benefical, grd.above_class_avg, grd.avg_class, grd.subject, grd.period, grd.id]]
        else:
            grd_list[grd.subject] = [[grd.actual_grade, grd.out_of, grd.coeff, grd.description, grd.benefical, grd.above_class_avg, grd.avg_class, grd.subject, grd.period, grd.id]]
    return grd_list
    # type : dict

# *********************
# *********************
"""
{"grades" : grades {subject: [[actual grade : float, grade.out_of : float, grade.coefficient : float, grade description : str, is grade good for subject average : bool, is grade over class average : bool, class average : float, subject name : str, period name : str]]} }
"""
# *********************
# UPDATING FUNCTIONS
# *********************

def update_grades_db(trim:int):
    """
    Updates the table Grades : adds only the grades that are not already in the database
    """
    existing_grades = Grades.query.all()
    new_grades = anal_grades(trim)
    existing_grade_specs = set((grade.description,grade.subject,grade.period) for grade in existing_grades)
    grades_to_add = [value for grade in new_grades for value in new_grades[grade] if (value[3],grade,value[7]) not in existing_grade_specs]
    for grd in grades_to_add:
        new_grade = Grades(actual_grade = grd[0], out_of = grd[1], coeff = grd[2], description = grd[3], benefical = grd[4], above_class_avg = grd[5], avg_class = grd[6], subject = grd[7], period = grd[8])
        db.session.add(new_grade)
    db.session.commit()
    # /!\ returns None

def update_subjects_db(trim:int):
    """
    Updates the table Subjects : adds only the subjects that are not already in the database
    """
    existing_subjects = Subjects.query.all()
    existing_subjects_names = set(subject.name for subject in existing_subjects)
    new_subjects = get_subjects(trim)
    subjects_avg = calc_avg_subject(trim)
    subjects_to_add = [subject for subject in new_subjects if subject not in existing_subjects_names]
    for sbj in subjects_to_add:
        new_subject = Subjects(name = sbj, avg = subjects_avg[sbj])
        db.session.add(new_subject)
    db.session.commit()
    # /!\ returns None

# *********************
# *********************
