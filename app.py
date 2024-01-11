from flask import render_template, url_for, request, redirect
from database import *
from main import *

login_failed = False

@app.before_request
def create_tables():
    db.create_all() #db creation

subjects = None
trimester = 1
inputs = None
periods = None

def get_content():
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
    global inputs
    global periods
    subjects = get_subjects(trimester)
    averages = calc_avg_subject(trimester)
    grades = anal_grades(trimester)
    inputs = {"subjects":subjects, "averages":averages, "grades":grades}
    periods = get_periods()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']
        try:
            get_data(input_username, input_password)
            get_content()
            return render_template('content.html', inputs=inputs, periods=periods)
        except pronotepy.exceptions.ENTLoginError:
            login_failed = True
            return render_template('login.html', login_failed=login_failed)
    else:
        return render_template("login.html")

@app.route('/period_selector', methods = ['POST', 'GET'])
def create_and_consult_db():
    global periods
    if request.method == 'POST':
        trim = periods[request.form['period_selector']]
        create_subjects_db(trim)
        create_averages_db(trim)
        create_grades_db(trim)
        sbj = extract_all_subjects_db()
        avg = extract_all_averages_db()
        grd = extract_all_grades_db()
        return render_template('blank.html', subjects = sbj, averages = avg, grades = grd)
    else:
        return render_template('blank.html')

if __name__=='__main__':
    app.run(debug=True)