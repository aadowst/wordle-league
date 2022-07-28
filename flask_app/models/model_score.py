

DATABASE = "wordle_league"

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import model_user


class Score:
    def __init__( self , data ):

        self.id = data['id']
        self.week = data['week']
        self.league_id = data['day']
        self.user_id = data['user1_id']

    @classmethod
    def save_score_model(cls, data):
        query = "INSERT INTO scores ( user_id, week, day1, day2, day3, day4, day5) VALUES ( %(user_id)s, %(week)s, %(day1)s, %(day2)s, %(day3)s, %(day4)s, %(day5)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_player_scores(cls,data):
        query= "SELECT * from scores where user_id = %(user_id)s and week = %(week)s;"
        
        player_scores = connectToMySQL(DATABASE).query_db( query, data )

        if player_scores:
            return player_scores[0]
        else:
            # if the player doesn't have any scores, add a new row
            query2 = "INSERT INTO scores ( user_id, week) VALUES ( %(user_id)s, %(week)s);"
            connectToMySQL(DATABASE).query_db( query2, data )
            return

    @classmethod
    def update_score_model(cls, data):


        query = "UPDATE scores SET day1 = %(day1)s, day2 = %(day2)s, day3 = %(day3)s, day4 = %(day4)s, day5 = %(day5)s where user_id = %(user_id)s and week = %(week)s;"
        return connectToMySQL(DATABASE).query_db( query, data )

