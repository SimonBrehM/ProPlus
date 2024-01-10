from flask import Flask, render_template, url_for, request, redirect
from database import *
from main import *

app = Flask(__name__)

login_failed = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

@app.before_request
def create_tables():
    db.create_all() #db creation

subjects = None
trimester = 1
inputs = None

def get_content():
    """
    Extracts data with pronotepy and inserts it into a global dictionnary (inputs)
    """
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