""" Modules and files imported """
from flask import render_template, url_for, request, redirect
from database2 import *
from main import *
from graphs import *

#default values
LOGIN_FAILED = False
RUN_COUNTER_PERIOD = None
INPUTS = None
EMPTY_TRIMESTER = False
USERNAME = None

@app.before_request
def create_tables():
    """
    Creates database
    """
    db.create_all() #database creation

def fill_tables_period(period:int, user:str): # time loss
    """
    Runs database update functions on first run
    """
    global RUN_COUNTER_PERIOD
    if RUN_COUNTER_PERIOD[period] == 0:
        create_averages_db(period, user)

def get_content_period(period:str, user:str): # time loss
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
    global INPUTS
    periods = get_periods()
    sbj_avg = calc_avg_subject(periods[period])[0]
    subject_averages = []
    for subject, average in sbj_avg.items():
        subject_averages.append([anal_subjects([subject])[0][0],
                                 average,
                                 period,
                                 anal_subjects([subject])[0][1]])
    grades = anal_grades(periods[period])
    averages = extract_period_averages_db(period, user)
    INPUTS = None
    INPUTS = {
            "subjects": subject_averages,
            #[[0:subjects name, 1:subject average, 2:trim,3: subject icon path], [ ... ]]
            "grades": grades,
            #[[
                # 0:grade value,
                # 1:out of?,
                # 2:grade coef,
                # 3:grade desc,
                # 4:grade benef,
                # 5:above class avg?,
                # 6:class avg,
                # 7:trim
                # ],
                # [ ... ]]
            "averages": averages, 
            #[[0:date, 1:trim, 2:overall average], [ ... ]]
            "periods": periods, 
            "current_period": get_current_period(),
            # "graph": moyenne_graph(72, 67)
            "graph": moyenne_graph(convert_to_100(float(averages[-1][2]), 20),
                                   convert_to_100(float(averages[-2][2]), 20) if len(averages) > 1
                                   else convert_to_100(float(averages[-1][2]), 20)),
            "suggestives": {}
            }

@app.route('/', methods=['POST', 'GET']) #root, login page
def index():
    """
    Connection to the ent
    """
    login_failed = request.args.get('login_failed')
    if login_failed:
        return render_template("login.html", login_failed=login_failed)
    return render_template("login.html")

@app.route('/content', methods = ['POST', 'GET']) #main page
def content():
    """
    Collects the data and displays it
    """
    if request.method == "POST":
        input_username = request.form['username']
        input_password = request.form['password']
        try:
            global RUN_COUNTER_PERIOD, USERNAME
            get_data(input_username, input_password) # connection to pronote
            USERNAME = input_username
            periods = get_periods() # {"period_name" : period_number}
            period = periods[get_current_period()] # current period number
            RUN_COUNTER_PERIOD = {period:0 for period in periods.values()}
            fill_tables_period(period, input_username) # filling db's tables
            RUN_COUNTER_PERIOD[period] += 1
            get_content_period(get_current_period(), input_username) # collecting all the data
            return render_template('content.html', inputs=INPUTS, empty_trimester=EMPTY_TRIMESTER)
        except pronotepy.exceptions.ENTLoginError and pronotepy.exceptions.PronoteAPIError:
            login_failed = True
            return redirect(url_for('index', login_failed=login_failed))
    return "HTTP redirect error"

def predict_grade(grade:float, out_of:float, coef:float, subject:str):
    """
    Returns a tuple with the predicted subject average and the predicted overall average
    """
    if grade > out_of:
        grade = out_of
    if grade < 0:
        grade = 0

    global INPUTS
    period = INPUTS["current_period"]

    subject_avg = [average[1] for average in INPUTS["subjects"] if average[0] == subject and average[2] == period]
    period_nb = INPUTS["periods"][period] # int
    subject_coeff = calc_avg_subject(period_nb)[1][anal_subjects([subject], True)[0]] # float
    new_subject_avg = round((float(subject_avg[0])*subject_coeff+grade) / (subject_coeff + coef), 2)
    all_avg = [float(i[1]) for i in INPUTS["subjects"] if i[2] == period and i[0] != subject and i[1] not in ("Absent","NonNote","Inapte","NonRendu","AbsentZero","NonRenduZero", "Dispense")]
    new_overall_avg = (sum(all_avg) + new_subject_avg) / (len(all_avg) + 1)

    return (round(new_subject_avg, 2), round(new_overall_avg, 2))
    # type tuple

@app.route('/suggest', methods = ['POST', 'GET'])
def suggestive():
    """
    Administrates the suggestive grades and displays them
    """
    global INPUTS, EMPTY_TRIMESTER

    grade, coef, subject = request.form['sgrade'], request.form['scoef'], request.form['subject']
    new_subject_avg, new_overall = predict_grade(str_to_float(grade),20,str_to_float(coef),subject)

    INPUTS['averages'].append([str(datetime.now()), INPUTS['current_period'], new_overall])
    INPUTS['graph'] = moyenne_graph(convert_to_100(float(INPUTS["averages"][-1][2]), 20), convert_to_100(float(INPUTS["averages"][-2][2]), 20), True)
    subject_index = (lambda list, subj: [i for i, v in enumerate(list) if v[0] == subj][0])(INPUTS['subjects'], subject)
    INPUTS['subjects'][subject_index][1] = new_subject_avg
    if subject not in INPUTS['suggestives']:
        INPUTS['suggestives'][subject] = []
    INPUTS['suggestives'][subject].append([grade, coef])

    return render_template('content.html', inputs=INPUTS, empty_trimester=EMPTY_TRIMESTER)

@app.route('/period_selector', methods = ['POST', 'GET'])
def create_and_consult_db():
    """
    Collects the data of a new period to display it
    """
    global INPUTS, RUN_COUNTER_PERIOD, EMPTY_TRIMESTER, USERNAME
    if request.method == 'POST':
        try:
            trimester = request.form['period_selector']
            EMPTY_TRIMESTER = False
            period = INPUTS["periods"][trimester]
            fill_tables_period(period, USERNAME)
            RUN_COUNTER_PERIOD[period] += 1
            get_content_period(trimester, USERNAME)
            INPUTS["current_period"] = trimester
            return render_template('content.html', inputs = INPUTS, empty_trimester=EMPTY_TRIMESTER)
        except ZeroDivisionError:
            EMPTY_TRIMESTER = True
            INPUTS["current_period"] = trimester
            return render_template('content.html', inputs = INPUTS, empty_trimester=EMPTY_TRIMESTER)

@app.route('/update_db', methods = ['POST', 'GET'])
def update_db():
    """
    Updates the db with the newest data
    """
    global INPUTS, USERNAME
    trimester = INPUTS["current_period"]
    get_content_period(trimester, USERNAME)
    return render_template('content.html', inputs=INPUTS, empty_trimester=EMPTY_TRIMESTER)

if __name__=='__main__':
    app.run(debug=True)
