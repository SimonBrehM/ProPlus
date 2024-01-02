from flask import Flask, render_template, url_for, request, redirect
from main import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
login_failed = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy()
db.init_app(app)

class Averages(db.Model):
    date = db.Column(db.DateTime, primary_key = True)
    period = db.Column(db.String)
    avg_overall = db.Column(db.Float)
    avg_subjects = db.Column(db.Float)

class Subjects(db.Model):
    name = db.Column(db.String, primary_key = True)
    avg = db.Column(db.Float)

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    actual_grade = db.Column(db.Float)
    out_of = db.Column(db.Float)
    coeff = db.Column(db.Float)
    description = db.Column(db.String)
    benefical = db.Column(db.Boolean)
    above_class_avg = db.Column(db.Boolean)
    avg_class = db.Column(db.Float, foreign_key = True)
    subject = db.Column(db.String, foreign_key = True)
    period = db.Column(db.String)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']
        try:
            get_data(input_username, input_password)
            return "success"
        except:
            login_failed = True
            return render_template('login.html', login_failed=login_failed)
        
    else:
        return render_template("login.html")

if __name__=='__main__':
    app.run(debug=True)