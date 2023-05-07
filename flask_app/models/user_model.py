from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')



class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at= data['created_at']
        self.updated_at = data['updated_at']
        
        
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s , %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return []

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) <1 :
            return False
        return cls(results[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def is_valid(users):
            is_valid = True
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query,users)
            if len(users['email']) <1 :
                flash("Email is required" , "register")
                is_valid = False
            if len(results) >= 1:
                flash("Email already taken" , "register")
                is_valid=False
            elif not EMAIL_REGEX.match(users['email']):
                flash("Invalid Email!", "register")
                is_valid=False
            if len(users['first_name']) <3:
                flash('First name must be 3 characters minimum!', "register")
                is_valid = False
            if len(users['last_name']) <3:
                flash(' Last name is required!', 'register')
                is_valid = False
            if len(users['password']) < 8:
                flash("Password must be 8 characters long", 'register')
                is_valid= False
            if not users['password'] == users['confirm']:
                flash("Passwords does not match", "register")
            return is_valid