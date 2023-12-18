from flask import Flask, render_template, url_for, request, redirect
from main import *

app = Flask(__name__)
login_failed = False

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