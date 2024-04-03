"""
Determines all database related functions and definitions.
"""
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main import *
# import os

def push_username(username):
    """
    Export username from database
    """
    global uid
    uid = username

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



# *********************
# TABLES OF THE DATABASE
# *********************

class Averages(db.Model):
    """
    Averages database object
    """
    user = db.Column(db.String, primary_key=True) # username
    date = db.Column(db.String, primary_key=True)
    # date when the data was inseted, format : YYYY-MM-DD HH-MM-SS.SSSSSS
    period = db.Column(db.String)
    avg_overall = db.Column(db.String)

def create_averages_db(trim:int, username:str):
    """
    Creation of an element in the table Averages coming from the period (trim)
    """
    avg = Averages(user = username,
                   date = str(datetime.now()),
                   period = trimester(trim).name,
                   avg_overall = calc_avg_overall(trim))
    db.session.add(avg)
    db.session.commit()
    # /!\ returns None

def extract_all_averages_db():
    """
    Extracts EVERY element from the table Averages and returns it on the form of a list
    """
    all_avg = Averages.query.all()
    avg_list = []
    for avg in all_avg:
        avg_list.append([avg.user, avg.date, avg.period, avg.avg_overall])
    return avg_list
    # type : list

def extract_period_averages_db(periode, username):
    """
    Extracts elements from the table Averages depending on the period
    and returns it on the form of a list
    """
    all_avg = Averages.query.filter_by(period=periode, user=username).all()
    avg_list = []
    for avg in all_avg:
        avg_list.append([avg.user, avg.date, avg.period, avg.avg_overall])
    return avg_list
    # type : list
