from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
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
            return render_template('sign_up.html')
        
@app.route('/sign_up', methods=['POST'])
def sign_up():
    new_username = request.form['username']
    new_password = request.form['password']

    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Credentials WHERE username = ? AND password = ?", (new_username, new_password))

        result = cursor.fetchone()

        if result:
            # Simulate a successful login
            return render_template('login_success.html', user=result)
        else:
            # Input new user into database
            cursor.execute("SELECT MAX(ID) FROM Credentials")
            new_ID = cursor.fetchone()[0] + 1
            
            cursor.execute("INSERT INTO Credentials (ID, username, password) VALUES (?, ?, ?)", (new_ID, new_username, new_password))
            return render_template('login_success.html', user=result)

def home():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()