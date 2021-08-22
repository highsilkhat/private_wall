from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

from flask_app.models.user import User
from flask_app.models.wall import Wall
from flask_app.controllers import walls

bcrypt = Bcrypt(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/users/create', methods = ['POST'])
def createAccount():
    
    if not User.validate_user(request.form):
            return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['newPassword'])
    data = {
            'first_name': request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password': pw_hash 
        }
    user = User.create_user(data)
    session['user_id'] = user
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session ['email'] = request.form['email']
        
    return redirect ('/wall')


@app.route('/users/login', methods = ['POST'])
def loginAccount():
    

    print(request.form)
    data = {
        'email': request.form['username']
    }

    user = User.getOneUserByEmail(data)
    
    if len(user) != 1:
        flash("Invalid username (email) or password entered")
        return redirect('/')

    user = user[0]
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid username (email) or password entered")
        return redirect('/')

    print (user.email)
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session ['email'] = user.email

    print(session)

    return redirect('/wall')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')