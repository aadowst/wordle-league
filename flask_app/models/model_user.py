# import the function that will return an instance of a connection
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z\s0-9_-]{3,15}$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-](?=.*?[0-9]).{8,}$')
# note:  name can have spaces; added \s to allow this

DATABASE = "wordle_league"

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

# model the class after the friend table from our database
class User:
    def __init__( self , data ):

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Now we use class methods to query our database



    @classmethod
    def save(cls, data ):

        query = "INSERT INTO users ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(DATABASE).query_db( query, data )

    # @classmethod
    # def get_all_not_user(cls, id):
    #     query = "SELECT * FROM users where id != %(id)s;"
    #     results = connectToMySQL(DATABASE).query_db(query, id)
    #     all_users = []
    #     # Iterate over the db results and create instances of friends with cls.
    #     for user in results:
    #         all_users.append( cls(user) )
    #     return all_users
    
    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"
    #     results = connectToMySQL(DATABASE).query_db(query)
    #     all_users = []
    #     # Iterate over the db results and create instances of friends with cls.
    #     for user in results:
    #         all_users.append( cls(user) )
    #     return all_users

    @classmethod
    def get_one_user(cls, data):

        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def email_match(cls, data):
        print("email to be found is:  ", data)
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print("the result is:  ",result)
        if not result:
            return False
        return cls(result[0])


    # @classmethod
    # def edit(cls, data):
    #     query = "UPDATE users SET name = %(name)s WHERE id = %(id)s;"
    #     return connectToMySQL(DATABASE).query_db( query, data)


    # @classmethod
    # def delete(cls, id):
    #     query = "DELETE FROM users WHERE id = %(id)s;"
    #     connectToMySQL(DATABASE).query_db(query, id)
    #     return


    @staticmethod
    def validate_registration(data):

        is_valid = True
        # if (len(data['first_name'])<3):
        #     flash("please enter at least two characters in first name", "registration")
        #     is_valid = False
        # elif not NAME_REGEX.match(data['first_name']):
        #     flash("only alphanumeric characters are allowed in first name", "registration")
        #     is_valid = False


        # if (len(data['last_name'])<3):
        #     flash("please enter at least two characters in last name", "registration")
        #     is_valid = False
        # elif not NAME_REGEX.match(data['last_name']):
        #     flash("only alphanumeric characters are allowed in last name", "registration")
        #     is_valid = False

        # if (len(data['email'])<1):
        #     flash("please enter an email address", "registration")
        #     is_valid = False
        # elif not EMAIL_REGEX.match(data['email']):
        #     flash("Email is not valid!", "registration")
        #     is_valid = False
        # elif User.email_match(data):
        #     flash("Email already entered!", "registration")
        #     is_valid = False


        # if not (data['password'] == data['confirm_password']):
        #     flash("Passwords do not match", "registration")
        #     is_valid = False
        # elif not PASSWORD_REGEX.match(data['password']):
        #     flash("Password must include a number and be 8 characters long", "registration")
        #     is_valid = False



        return is_valid