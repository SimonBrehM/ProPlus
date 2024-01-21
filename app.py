from flask import render_template, url_for, request, redirect
from database import *
from main import *

login_failed = False
run_counter = 0
run_counter_period = None

@app.before_request
def create_tables():
    db.create_all() #db creation

def fill_tables():
    global run_counter
    if run_counter == 0:
        update_subjects_db(1)
        create_averages_db(1)
        update_grades_db(1)

def fill_tables_period(period:int):
    global run_counter_period
    if run_counter_period[period] == 0:
        update_subjects_db(period)
        create_averages_db(period)
        update_grades_db(period)

subjects = None
trimester = 1
inputs = None
periods = None

def get_content():
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
    global inputs, periods, run_counter_period
    subject_averages = extract_all_subjects_db()
    grades = extract_all_grades_db()
    averages = extract_all_averages_db()
    inputs = {"subjects":subject_averages, "grades":grades, "averages":averages}
    periods = get_periods()
    run_counter_period = {period:0 for period in periods.values()}

def get_content_period(period:str):
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
    global inputs
    subject_averages = extract_period_subjects_db(period)
    grades = extract_period_grades_db(period)
    averages = extract_period_averages_db(period)
    inputs = None
    inputs = {"subjects":subject_averages, "grades":grades, "averages":averages}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']
        try:
            global run_counter
            get_data(input_username, input_password)
            fill_tables()
            run_counter += 1
            get_content()
            return render_template('content.html', inputs=inputs, periods=periods)
        except pronotepy.exceptions.ENTLoginError:
            login_failed = True
            return render_template('login.html', login_failed=login_failed)
    else:
        return render_template("login.html")

@app.route('/period_selector', methods = ['POST', 'GET'])
def create_and_consult_db():
    global periods, inputs, run_counter_period
    if request.method == 'POST':
        trimester = request.form['period_selector']
        period = periods[trimester]
        fill_tables_period(period)
        run_counter_period[period] += 1
        get_content_period(trimester)
        return inputs
    else:
        return render_template('content.html', inputs = inputs, periods=periods)

@app.route('/update_db', methods = ['POST', 'GET'])
def update_db():
    global trimester, periods, inputs
    update_grades_db(trimester)
    update_subjects_db(trimester)
    get_content()
    return render_template('content.html', inputs=inputs, periods=periods)

# @app.route('/remove_db', methods = ['POST','GET'])
# def remove_db_btn():
#     if request.method == 'POST':
#         remove_db()
#         return 'db removed'
#     else:
#         return render_template('blank.html')

# def predict_grade(grade:float, out_of:float, subject:int, period:int): # subject : position in a list
#     prediction = []
#     global inputs, periods #new
#     sbj_avg = 0
#     period_name = lambda periods: [i for i in periods if periods[i] == period] # new
#     sbj_coeff = calc_avg_subject(period)[1][sbj_name(periods)[0]] # new
#     new_sbj_avg = (sbj_avg * sbj_coeff + grade) / (sbj_coeff + out_of)
#     all_avg = [i[1] for i in inputs["subjects"] if i[2] == trimestre(period)]

#     return prediction
#     # type list

if __name__=='__main__':
    app.run(debug=True)
