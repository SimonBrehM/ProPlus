from flask import render_template, url_for, request, redirect
from database import *
from main import *
from graphs import *

#default values
login_failed = False
run_counter_period = None
inputs = None
empty_trimester = False

@app.before_request
def create_tables():
    db.create_all() #database creation

def fill_tables_period(period:int): # time loss
    global run_counter_period
    if run_counter_period[period] == 0:
        update_subjects_db(period)
        create_averages_db(period)
        update_grades_db(period)

def get_content_period(period:str): # time loss
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
    global inputs
    subject_averages = extract_period_subjects_db(period)
    grades = extract_period_grades_db(period)
    averages = extract_period_averages_db(period)
    inputs = None
    print("---->", averages[-1][2])
    inputs = {
            "subjects": subject_averages, #[[0:subjects name, 1:subject average, 2:trim,3: subject icon path], [ ... ]]
            "grades": grades, #[[0:grade value, 1:out of?, 2:grade coef, 3:grade desc, 4:grade benef, 5:above class avg?, 6:class avg, 7:trim], [ ... ]]
            "averages": averages, #[[0:date, 1:trim, 2:overall average], [ ... ]]
            "periods": get_periods(), 
            "current_period": get_current_period(),
            # "graph": moyenne_graph(72, 67)
            "graph": moyenne_graph(convert_to_100(float(averages[-1][2]), 20), convert_to_100(float(averages[-2][2]), 20) if len(averages) > 1 else convert_to_100(float(averages[-1][2]), 20))
            }

@app.route('/', methods=['POST', 'GET']) #root, login page
def index():
    login_failed = request.args.get('login_failed')
    if login_failed:
        return render_template("login.html", login_failed=login_failed)
    else:
        return render_template("login.html")

@app.route('/content', methods = ['POST', 'GET']) #main page
def content():
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']
        try:
            global run_counter_period
            get_data(input_username, input_password)
            periods = get_periods()
            period = periods[get_current_period()]
            run_counter_period = {period:0 for period in periods.values()}
            fill_tables_period(period)
            run_counter_period[period] += 1
            get_content_period(get_current_period())
            print(inputs["grades"])
            return render_template('content.html', inputs=inputs, empty_trimester=empty_trimester)
        except pronotepy.exceptions.ENTLoginError and pronotepy.exceptions.PronoteAPIError:
            login_failed = True
            return redirect(url_for('index', login_failed=login_failed))
    else:
        return "HTTP redirect error"

@app.route('/period_selector', methods = ['POST', 'GET'])
def create_and_consult_db():
    global inputs, run_counter_period, empty_trimester
    if request.method == 'POST':
        try:
            trimester = request.form['period_selector']
            empty_trimester = False
            period = inputs["periods"][trimester]
            fill_tables_period(period)
            run_counter_period[period] += 1
            get_content_period(trimester)
            inputs["current_period"] = trimester
            return render_template('content.html', inputs = inputs, empty_trimester=empty_trimester)
        except ZeroDivisionError:
            empty_trimester = True
            inputs["current_period"] = trimester
            return render_template('content.html', inputs = inputs, empty_trimester=empty_trimester)

@app.route('/update_db', methods = ['POST', 'GET'])
def update_db():
    global inputs
    trimester = inputs["current_period"]
    update_grades_db(inputs["periods"][trimester])
    update_subjects_db(inputs["periods"][trimester])
    get_content_period(trimester)
    return render_template('content.html', inputs=inputs, empty_trimester=empty_trimester)

def predict_grade(grade:float, out_of:float, subject:str):
    """
    Returns a tuple with the predicted subject average and the predicted overall average
    """
    # subject : result from a selector ?
    if grade > out_of:
        grade = out_of
    if grade < 0:
        grade = 0
    
    global inputs
    period = inputs["current_period"]
    
    subject_avg = [average[1] for average in inputs["subjects"] if average[0] == subject and average[2] == period]
    period_nb = inputs["periods"][period] # int
    
    subject_coeff = calc_avg_subject(period_nb)[1][subject] # float | modify creation and extraction functions so it's added to the db and in inputs ?
    new_subject_avg = (subject_avg[0] * subject_coeff + grade) / (subject_coeff + out_of)
    all_avg = [i[1] for i in inputs["subjects"] if i[2] == period and i[0] != subject]
    new_overall_avg = (sum(all_avg) + new_subject_avg) / len(all_avg) + 1

    return (new_subject_avg, new_overall_avg)
    # type tuple

if __name__=='__main__':
    app.run(debug=True)
