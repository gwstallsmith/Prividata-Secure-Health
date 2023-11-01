from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def check_credentials():
    input_username = request.form['username']
    input_password = request.form['password']
    
    with sqlite3.connect("db.sqlite3") as connection:

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Credentials WHERE username = ? AND password = ?", (input_username, input_password))

        result = cursor.fetchone()

        if result:
            # Simulate a successful login
            return render_template('login_success.html', user=result)
        else:
            # Simulate an incorrect login
            return render_template('login_failure.html')
        





def home():
    return render_template('login.html')

#def hello_world():
#    return "Hello, world"

if __name__ == '__main__':
    app.run()