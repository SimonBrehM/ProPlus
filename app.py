from flask import Flask, render_template, url_for, request, redirect
from main import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
login_failed = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Averages(db.Model):
    date = db.Column(db.String, primary_key=True) # date when the data was inseted, format : YYYY-MM-DD HH-MM-SS.SSSSSS
    period = db.Column(db.String)
    avg_overall = db.Column(db.Float)

class Subjects(db.Model):
    name = db.Column(db.String, primary_key = True)
    avg = db.Column(db.Float)

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    actual_grade = db.Column(db.Float)
    out_of = db.Column(db.Float)
    coeff = db.Column(db.Float)
    description = db.Column(db.String)
    benefical = db.Column(db.Boolean) # grade > subject_avg
    above_class_avg = db.Column(db.Boolean) # grade > class_avg
    avg_class = db.Column(db.Float)
    subject = db.Column(db.String)
    period = db.Column(db.String)

@app.before_request
def create_tables():
    db.create_all() #db creation

def create_subjects_db(trim:int): # creation and filling table "Subjects"
    subjects_avg = calc_avg_subject(trim)
    for subject in subjects_avg.keys():
        sbj = Subjects(name = subject, avg = subjects_avg[subject])
        db.session.add(sbj)
        db.session.commit()

def create_averages_db(trim:int): # creation and filling table "Averages"
    avg = Averages(date = str(datetime.now()), period = trimestre(trim).name(), avg_overall = calc_overall_avg(trim))
    db.session.add(avg)
    db.session.commit()

def create_grades_db(trim:int): # creation and filling table "Grades"
    all_grades = grades_specs(trim)
    trim_str = trimestre(trim).name()
    for sbj in all_grades:
        for grd in all_grades[sbj]:
            grade = Grades(actual_grade = grd[0], out_of = grd[1], coeff = grd[2], description = grd[3], benefical = grd[4], above_class_avg = grd[5], avg_class = grd[6], subject = sbj, period = trim_str)
            db.session.add(grade)
            db.session.commit()

def commit_averages_db(avg_period, avg_avg_overall): # adding 1 elt to table "Averages"
    avg = Averages(date = str(datetime.now()), period = avg_period, avg_overall = avg_avg_overall)
    db.session.add(avg)
    db.session.commit()

def commit_subjects_db(sbj_name, sbj_avg): # adding 1 elt to table "Subjects"
    subject = Subjects(name = sbj_name, avg = sbj_avg)
    db.session.add(subject)
    db.session.commit()

def commit_grades_db(grd_actual_grade, grd_out_of, grd_coeff, grd_desc, grd_benef, grd_above_class, grd_class_avg, grd_sbj, grd_period): # adding 1 elt to table "Grades"
    grade = Grades(actual_grade = grd_actual_grade, out_of = grd_out_of, coeff = grd_coeff, description = grd_desc, benefical = grd_benef, above_class_avg = grd_above_class, avg_class = grd_class_avg, subject = grd_sbj, period = grd_period)
    db.session.add(grade)
    db.session.commit()

def extract_all_averages_db():
    all_avg = Averages.query.all()
    avg_list = []
    for avg in all_avg:
        avg_list.append(avg.date, avg.period, avg.avg_overall)
    return avg_list

def extract_all_subjects_db():
    all_sbj = Subjects.query.all()
    sbj_list = []
    for sbj in all_sbj:
        sbj_list.append(sbj.name, sbj.avg)
    return sbj_list

def extract_all_grades_db():
    all_grd = Grades.query.all()
    grd_list = []
    for grd in all_grd:
        grd_list.append(grd.id, grd.actual_grade, grd.out_of, grd.coeff, grd.description, grd.benefical, grd.above_class_avg, grd.avg_class, grd.subject, grd.period)
    return grd_list

subjects = None
trimester = 1
inputs = None

def get_content():
    global inputs
    subjects = get_subjects(trimester)
    averages = calc_avg_subject(trimester)
    grades = grades_specs(trimester)
    inputs = {"subjects":subjects, "averages":averages, "grades":grades}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']
        try:
            get_data(input_username, input_password)
            get_content()
            return render_template('content.html', inputs=inputs)
        except pronotepy.exceptions.ENTLoginError:
            login_failed = True
            return render_template('login.html', login_failed=login_failed)
    else:
        return render_template("login.html")

if __name__=='__main__':
    app.run(debug=True)