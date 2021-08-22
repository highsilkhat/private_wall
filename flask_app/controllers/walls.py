from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

from flask_app.models.user import User
from flask_app.models.wall import Wall
from flask_app.controllers import users

@app.route('/wall')
def wall():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    recipients = Wall.get_outbox(data)
    # outbox_length = (len(recipients))
    inbox = Wall.get_inbox(data)
    inbox_length = (len(inbox))

    return render_template('wall.html', recipients = recipients, inbox = inbox, inbox_length = inbox_length)

@app.route('/post/message/<int:recipient_id>', methods = ['POST'])
def post_message(recipient_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    if not Wall.verify_message(request.form):
        return redirect('/wall')
    data = {

        'sender_id': session['user_id'],
        'recipient_id': recipient_id,
        'message' : request.form['message']
    }

    Wall.send_message(data)

    return redirect ('/wall')

@app.route('/delete/message/<int:message_id>')
def delete_message(message_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    data = {

        'id':message_id
    }

    Wall.delete_message(data)

    return redirect('/wall')