from flask import render_template, url_for, request, redirect
from database import *
from main import *

login_failed = False
run_counter = 0
run_counter_period = None

@app.before_request
def create_tables():
    db.create_all() #db creation

def fill_tables_period(period:int): # time loss
    global run_counter_period
    if run_counter_period[period] == 0:
        update_subjects_db(period)
        create_averages_db(period)
        update_grades_db(period)

inputs = None
periods = None
bad_period = False


def get_content_period(period:str): # time loss
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
    global inputs, periods, run_counter_period
    subject_averages = extract_period_subjects_db(period)
    grades = extract_period_grades_db(period)
    averages = extract_period_averages_db(period)
    inputs = None
    inputs = {"subjects":subject_averages, "grades":grades, "averages":averages, "periods":periods, "current_period":get_current_period()}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']
        try:
            global periods, run_counter_period
            get_data(input_username, input_password)
            # push_username(input_username)
            periods = get_periods()
            period = periods[get_current_period()]
            run_counter_period = {period:0 for period in periods.values()}
            fill_tables_period(period)
            run_counter_period[period] += 1
            get_content_period(get_current_period())
            return render_template('content.html', inputs=inputs, bad_period=bad_period)
        except pronotepy.exceptions.ENTLoginError:
            login_failed = True
            return render_template('login.html', login_failed=login_failed)
    else:
        return render_template("login.html")

@app.route('/period_selector', methods = ['POST', 'GET'])
def create_and_consult_db():
    global periods, inputs, run_counter_period, bad_period
    if request.method == 'POST':
        try:
            trimester = request.form['period_selector']
            bad_period = False
            period = periods[trimester]
            fill_tables_period(period)
            run_counter_period[period] += 1
            get_content_period(trimester)
            inputs["current_period"] = trimester
            return render_template('content.html', inputs = inputs, bad_period=bad_period)
        except ZeroDivisionError:
            bad_period = True
            inputs["current_period"] = trimester
            return render_template('content.html', inputs = inputs, bad_period=bad_period)

@app.route('/update_db', methods = ['POST', 'GET'])
def update_db():
    global periods, inputs
    trimester = inputs["current_period"]
    update_grades_db(periods[trimester])
    update_subjects_db(periods[trimester])
    get_content_period(trimester)
    return render_template('content.html', inputs=inputs, bad_period=bad_period)


def predict_grade(grade:float, out_of:float, subject:str):
    """
    Returns a tuple with the predicted subject average and the predicted overall average
    """
    # subject : result from a selector ?
    global inputs
    period = inputs["current_period"]
    subject_avg = [average[1] for average in inputs["subjects"] if average[0] == subject and average[2] == period]
    period_nb = periods[period] # int
    subject_coeff = calc_avg_subject(period_nb)[1][subject] # float | modify creation and extraction functions so it's added to the db and in inputs ?
    new_subject_avg = (subject_avg[0] * subject_coeff + grade) / (subject_coeff + out_of)
    all_avg = [i[1] for i in inputs["subjects"] if i[2] == period and i[0] != subject]
    new_overall_avg = (sum(all_avg) + new_subject_avg) / len(all_avg) + 1
    return (new_subject_avg, new_overall_avg)
    # type tuple

if __name__=='__main__':
    app.run(debug=True)
