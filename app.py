from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

users = [
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = None
    for u in users:
        if u['username'] == username and u['password'] == password:
            user = u
            break

    if user:
        # Simulate a successful login
        return render_template('login_success.html', user=user)
    else:
        # Simulate an incorrect login
        return render_template('login_failure.html')

def home():
    return render_template('login.html')

#def hello_world():
#    return "Hello, world"

if __name__ == '__main__':
    app.run()