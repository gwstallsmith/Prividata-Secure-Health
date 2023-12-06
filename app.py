from flask import Flask, render_template, request, make_response, redirect, url_for
import sqlite3

from crypto import *
from utils import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index_page():
    response = make_response(render_template('index.html', error = None))
    return response

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html', error = None)

@app.route('/check_credentials', methods=['GET', 'POST'])
def check_credentials():
    error = None
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']
        
        with sqlite3.connect("db.sqlite3") as connection:

            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Credentials WHERE Username = ? AND Password = ?", (input_username, hash_password(input_password)))
    
            result = cursor.fetchone()
            
        if result:
            # Simulate a successful login
            user = result
            # Store user information in a cookie
            response = make_response(render_template('index.html', user=user, logged_in=True))

            response.set_cookie('ID', str(user[0]))
            response.set_cookie('Username', str(user[1]))

            generate_shared_secret(input_password)

            return response
        else:
            # Simulate an incorrect login
            error = "Invalid user credentials"
        
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # Clear the cookies by creating a response and deleting the cookies
    response = make_response(redirect(url_for('index_page')))  # Redirect to home page
    response.set_cookie('ID', '', expires = 0)  # Clear 'ID' cookie
    response.set_cookie('Username', '', expires = 0)  # Clear 'Username' cookie
    return response


@app.route('/sign_up')
def sign_up_form():
    return render_template('sign_up.html')
        
@app.route('/sign_up', methods=['POST'])
def sign_up():
    sign_up_form()
    new_username = request.form['username']
    new_password = request.form['password']

    first_name = request.form['firstname']
    last_name = request.form['lastname']

    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Credentials WHERE Username = ? AND Password = ?", (new_username, hash_password(new_password)))

        result = cursor.fetchone()

        # When the user signing up exists in db
        if result:
            # Simulate a successful login
            # Store user information in a cookie
            response = make_response(render_template('index.html', user=result, logged_in=True))

            response.set_cookie('ID', str(result[0]))
            response.set_cookie('Username', str(result[1]))
            generate_shared_secret(new_password)


        # Otherwise user does not exist
        # Need to sign them up
        else:
            # Input new user into database
            cursor.execute("SELECT MAX(ID) FROM Credentials")
            new_ID = cursor.fetchone()[0] + 1
            
            cursor.execute("INSERT INTO Credentials (ID, Username, Password) VALUES (?, ?, ?)", (new_ID, new_username, hash_password(new_password)))
            cursor.execute("INSERT INTO PatientInformation (ID, First_Name, Last_Name) VALUES (?, ?, ?)", (new_ID, first_name, last_name))

            response = make_response(render_template('index.html', user=result, logged_in=True))

            response.set_cookie('ID', str(new_ID))
            response.set_cookie('Username', new_username)
            generate_shared_secret(new_password)

        return response


@app.route('/patient_info', methods=['GET', 'POST'])
def display_info():
    # Check if 'ID' and 'Username' cookies are present


    if 'ID' in request.cookies and 'Username' in request.cookies:
        user_id = request.cookies.get('ID')

        with sqlite3.connect("db.sqlite3") as connection:
            cursor = connection.cursor()

            # Check if the user is an admin (you might have a column like 'IsAdmin' in your Credentials table)
            cursor.execute("SELECT * FROM Credentials WHERE ID = ?", (user_id,))
            user = cursor.fetchone()

            if user and user[3] == 2:
                # User is an admin, display all users
                forms = cursor.execute("SELECT * FROM PatientInformation").fetchall()
                admin_data = cursor.execute("SELECT * FROM PatientInformation WHERE ID = ?", (user[0],)).fetchone()

                try:
                    admin_data = admin_data + (admin_data[0],) + (decrypt(admin_data[1]),) + (decrypt(admin_data[2]),) + (decrypt(admin_data[3]),) + (admin_data[4],) + (admin_data[5],) + (admin_data[6],) + (decrypt(admin_data[7]),)
                except KeyError:
                    return render_template('login.html', error = "Shared secret expired.")
                
                return render_template('patient_info.html', users = forms, id = user[0], admin = admin_data)
            else:
                # User is not an admin, display single user
                user_data = cursor.execute("SELECT * FROM PatientInformation WHERE ID = ?", (user_id,)).fetchone()

                try:
                    user_data_decrypt = user_data + (user_data[0],) + (decrypt(user_data[1]),) + (decrypt(user_data[2]),) + (decrypt(user_data[3]),) + (user_data[4],) + (user_data[5],) + (user_data[6],) + (decrypt(user_data[7]),)
                except KeyError:
                    return render_template('login.html', error = "Shared secret expired.")

                if verify_mac(decrypt(user_data[7]), decrypt(user_data[8])):
                    return render_template('patient_info.html', user = user_data_decrypt)
                else:
                    error = "MAC verification failed. Data integrity not guaranteed."
                    return render_template('patient_info.html', user = user_data_decrypt, error = error)

    else:
        # If cookies are not present, redirect to login page or handle the situation accordingly
        return redirect('/login')
    

@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.cookies.get('ID')
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']

    age = request.form['age']
    weight = request.form['weight']
    height = request.form['height']

    try:
        health_history = encrypt(request.form['health_history'])
    except KeyError:
        return render_template('login.html', error = "Shared secret expired.")
    

    print(request.form['health_history'])

    mac = encrypt(generate_mac(request.form['health_history']))

    # Update user in the database
    query = """
    UPDATE PatientInformation 
    SET First_Name = ?, Last_Name = ?, Gender = ?, Age = ?, Weight = ?, Height = ?, Health_History = ?, MAC = ?
    WHERE ID = ?
    """

    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute(query, (encrypt(first_name), encrypt(last_name), encrypt(gender), age, weight, height, health_history, mac, user_id))
        connection.commit()
    
    return redirect('/patient_info')

@app.route('/more', methods=['POST', 'GET'])
def more():
    return
    generate_more_users()


if __name__ == '__main__':
    app.run()