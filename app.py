from flask import render_template, url_for, request, redirect
from database import *
from main import *

login_failed = False
run_counter = 0

@app.before_request
def create_tables():
    db.create_all() #db creation

def fill_tables():
    global run_counter
    if run_counter == 0:
        update_subjects_db(1)
        create_averages_db(1)
        update_grades_db(1)


subjects = None
trimester = 1
inputs = None
periods = None

def get_content():
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
    global inputs, periods
    subject_averages = extract_all_subjects_db()
    grades = extract_all_grades_db()
    averages = extract_all_averages_db()
    inputs = {"subjects":subject_averages, "grades":grades, "averages":averages}
    periods = get_periods()

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
    global periods, trimester
    if request.method == 'POST':
        trimester = periods[request.form['period_selector']]
        sbj = extract_all_subjects_db()
        avg = extract_all_averages_db()
        grd = extract_all_grades_db()
        return render_template('blank.html', subjects = sbj, averages = avg, grades = grd)
    else:
        return render_template('blank.html')

@app.route('/update_db', methods = ['POST', 'GET'])
def update_db():
    global trimester, periods, inputs
    update_grades_db(trimester)
    update_subjects_db(trimester)
    get_content()
    return render_template('content.html', inputs=inputs, periods=periods)

def predict_grade(grade:float, out_of:float, subject:int, period:int): # subject : position in a list
    prediction = []
    global inputs
    subject_avg = inputs["subjects"][subject][1]
    subject_coeff = calc_avg_subject(period)[1][subjectname]
    

    return prediction
    # type list

if __name__=='__main__':
    app.run(debug=True)