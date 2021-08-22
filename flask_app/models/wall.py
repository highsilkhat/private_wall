from flask.helpers import is_ip
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
import re

from flask_app.models import user

class Wall:
    def __init__(self, data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.recipent_id = data['recipient_id']
        self.message = data['message']
        self.created_at =  data['created_at']
        self.updated_at = data['updated_at']
        self.sender = []
        self.recipent = []

    @classmethod
    def get_outbox(cls, data):
    
        query = 'SELECT * FROM users ORDER BY last_name DESC;'
       # query = 'SELECT * FROM messages LEFT JOIN users ON messages.recipient_id = users.id WHERE sender_id = %(id)s;'

        results = connectToMySQL('private_wall_schema').query_db(query, data)


        users = []

        for item in results:
            users.append (user.User (item))
        return users

        # messages = []

        # for message in results:
        #     new_message = Wall(message)
        #     recipients_data = {
        #         'id': message['users.id'],
        #         'first_name': message['first_name'],
        #         'last_name': message['last_name'],
        #         'email': message['email'],
        #         'password': message['password'],
        #         'created_at': message['users.created_at'],
        #         'updated_at': message['users.updated_at']
        #     }
        #     recipient = user.User(recipients_data)
        #     new_message.recipient = recipient
        #     messages.append(new_message)

        return messages

    @classmethod
    def send_message(cls, data):
        query = 'INSERT INTO messages (sender_id, recipient_id, message) VALUES (%(sender_id)s,%(recipient_id)s, %(message)s);'
        
        connectToMySQL('private_wall_schema').query_db(query, data)
        flash ("Message successfully sent!")

    @classmethod
    def get_inbox(cls, data):
        query = 'SELECT * FROM messages JOIN users ON messages.sender_id = users.id WHERE messages.recipient_id = %(id)s ORDER BY last_name DESC;'

        results = connectToMySQL('private_wall_schema').query_db(query, data)

        messages = []

        for message in results:
            new_message = Wall(message)
            senders_data = {
                'id': message['users.id'],
                'first_name': message['first_name'],
                'last_name': message['last_name'],
                'email': message['email'],
                'password': message['password'],
                'created_at': message['users.created_at'],
                'updated_at': message['users.updated_at']
            }
            sender = user.User(senders_data)
            new_message.sender = sender
            messages.append(new_message)

        return messages


    @staticmethod
    def delete_message(data):
        query = 'DELETE FROM messages WHERE id = %(id)s;'
        
        connectToMySQL('private_wall_schema').query_db(query, data)


    @staticmethod
    def verify_message(data):
        is_valid = True

        if len(data['message']) < 5:
            is_valid = False
            flash('Messages must be at leat 5 characters in length')
    
        return is_valid

