from flask import Flask, redirect , url_for, render_template, request, flash
from model import db, Users
from config import Config
import os, subprocess, re

#def create_database():
    # Run the create_database.py script
 #   subprocess.run(['python', 'create_db.py'], check=True)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def is_valid_password(password):
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

# Create the database before running the app
#with app.app_context():
 #   create_database()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/sign-in", methods=['GET', 'POST'])
def signin():
    return render_template('sign-in.html')

@app.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method== 'POST': 
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not is_valid_password(password):
            flash('Password criteria not met. Look at passowrd description')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))
        
        if Users.query.filter_by(username=username).first():
            flash('Username already exists! Try using a different username.')
            return redirect(url_for('signup'))

        new_user = Users(username=username, email=email, firstname=firstname, lastname=lastname, password=password)
            #new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('thankyou.html',firstname=firstname,lastname=lastname )
    return render_template('sign-up.html')

@app.route("/flasherror")
def flasherror():
    return render_template('flasherror.html')

@app.route("/thankyou", methods=['GET', 'POST'])
def thankyou():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    return render_template('thankyou.html',firstname=firstname,lastname=lastname )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()