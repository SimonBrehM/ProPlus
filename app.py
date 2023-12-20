from flask import Flask, render_template, url_for, request, redirect
from main import *

app = Flask(__name__)

login_failed = False
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