from flask import Flask, render_template, request, jsonify
import sqlite3

import hashlib

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

        cursor.execute("SELECT * FROM Credentials WHERE Username = ? AND Password = ?", (input_username, hash_password(input_password)))

        result = cursor.fetchone()

        if result:
            # Simulate a successful login
            return render_template('login_success.html', user=result)
        else:
            # Simulate an incorrect login
            return render_template('sign_up.html')
        


# Function hash ALL PASSWORDS in database
def salt_passwords():
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT Username, Password FROM Credentials")
        result = cursor.fetchall()

        for user in result:
            salted_password = hash_password(user[1])
            cursor.execute("UPDATE Credentials SET Password = ? WHERE Username = ?", (salted_password, user[0]))



# Function to get the result of hashing a password
def hash_password(password):
    # Encode for hashing to work
    password = password.encode('utf-8')

    hash = hashlib.sha256()         # Create Hashing object
    hash.update(password)           # Apply hashing algorithm
    hash_pass = hash.hexdigest()    # Use hex representation

    return hash_pass

        
@app.route('/sign_up', methods=['POST'])
def sign_up():
    new_username = request.form['username']
    new_password = request.form['password']

    first_name = request.form['firstname']
    last_name = request.form['lastname']


    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Credentials WHERE Username = ? AND Password = ?", (new_username, hash_password(new_password)))

        result = cursor.fetchone()

        if result:
            # Simulate a successful login
            return render_template('login_success.html', user=result)
        else:
            # Input new user into database
            cursor.execute("SELECT MAX(ID) FROM Credentials")
            new_ID = cursor.fetchone()[0] + 1
            
            cursor.execute("INSERT INTO Credentials (ID, Username, Password) VALUES (?, ?, ?)", (new_ID, new_username, hash_password(new_password)))
            cursor.execute("INSERT INTO PatientInformation (ID, First_Name, Last_Name) VALUES (?, ?, ?)", (new_ID, first_name, last_name))
        
            return render_template('login_success.html', user=result)
        
@app.route('/patient_info', methods=['POST'])
def display_info():
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        
        # IF cookie says admin display all users
        # ELSE cookie says no admin display single user



def remove_user(id):
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Credentials WHERE ID = ?", (id,))


def home():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()