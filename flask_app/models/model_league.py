

DATABASE = "wordle_league"

from random import randint
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import model_user


class League:
    def __init__( self , data ):

        self.id = data['id']
        self.name = data['name']
        self.length = data['length']
        self.capacity = data['capacity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.players = []



    @classmethod
    def save(cls, data1 ):

        query1 = "INSERT INTO leagues ( name, length, capacity) VALUES ( %(name)s, %(length)s, %(capacity)s);"
        league_id = connectToMySQL(DATABASE).query_db( query1, data1 )
        query2 = "INSERT INTO users_in_leagues (user_id, league_id, user_level) values (%(user_id)s, %(league_id)s, %(user_level)s)"
        data2 = {
            "user_id": session["user_id"],
            "league_id":  league_id,
            "user_level": 9
        }
        connectToMySQL(DATABASE).query_db( query2, data2 )
        return

    @classmethod
    def model_join_league(cls, data):
        # add a check to see if the user is already in the league. if so, return an error that can be flashed on the page
        query = "INSERT INTO users_in_leagues (user_id, league_id, user_level) values (%(user_id)s, %(league_id)s, %(user_level)s)"
        data = {
            "user_id": session["user_id"],
            "league_id": data["league_id"],
            "user_level": 1
        }
        connectToMySQL(DATABASE).query_db( query, data )
        return

    
    @classmethod
    def get_all_leagues(cls):
        query = "SELECT * FROM leagues;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_leagues = []
        for league in results:
            all_leagues.append( cls(league) )
        return all_leagues

    @classmethod
    def get_my_leagues(cls, data):

        query = "SELECT * FROM users_in_leagues join leagues on users_in_leagues.league_id = leagues.id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print("model_league line 65, results are:  ", results)
        my_leagues = []
        for league in results:
            my_leagues.append( cls(league) )
        return my_leagues

    @classmethod
    def get_not_my_leagues(cls, data):

        query = "SELECT * FROM leagues LEFT JOIN users_in_leagues on users_in_leagues.league_id = leagues.id WHERE users_in_leagues.league_id NOT IN (SELECT league_id FROM users_in_leagues join leagues on users_in_leagues.league_id = leagues.id WHERE users_in_leagues.user_id = %(user_id)s) GROUP BY league_id"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            not_my_leagues = []
            for league in results:
                not_my_leagues.append( cls(league) )
            return not_my_leagues
        else:
            return
        
    @classmethod
    def get_league_with_players(cls, data):
        query = "SELECT * from leagues JOIN users_in_leagues on leagues.id = users_in_leagues.league_id join users on users_in_leagues.user_id = users.id WHERE leagues.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        one_league= cls(results[0])

        for row_from_db in results:
            player = {
                "id": row_from_db["users.id"],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "email": row_from_db["email"],
                "password": row_from_db['password'],
                "created_at": row_from_db['created_at'],
                "updated_at": row_from_db['updated_at']
            }
            one_league.players.append(model_user.User(player))
        return one_league

    @classmethod
    def get_player_records(cls, data):
        query = "SELECT * from users LEFT JOIN matchups users.id = matchups.user_id where matchups.league_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        one_league= cls(results[0])

        for row_from_db in results:
            player = {
                "id": row_from_db["users.id"],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "email": row_from_db["email"],
                "password": row_from_db['password'],
                "created_at": row_from_db['created_at'],
                "updated_at": row_from_db['updated_at']
            }
            one_league.players.append(model_user.User(player))
        return one_league


    @classmethod
    def update_league_model(cls, data):
        query = "UPDATE leagues SET name = %(name)s, length = %(length)s, capacity = %(capacity)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db( query, data)


    @classmethod
    def create_schedule(cls, id):
        # delete any existing matchups that exist
        data_delete = {"league_id": id}
        query_delete = "DELETE FROM matchups WHERE league_id = %(league_id)s;"
        connectToMySQL(DATABASE).query_db(query_delete, data_delete)

        # create all new matchups
        one_league = League.get_league_with_players({"id": id})
        week = 1
        while week <= one_league.length:
            unmatched_players = []
            # for loop creates fills the list with the indexes of the players in the league
            for i in range(len(one_league.players)):
                unmatched_players.append(i)
            # pops random indexes from the list of unmatched players and assigns user1 and user2 the ids of the players at those indexes. repeats this process until there are 0 or 1 numbers left in the list
            while len(unmatched_players)>=2:
                popped_num = unmatched_players.pop(randint(0, len(unmatched_players)-1))
                popped_num2 = unmatched_players.pop(randint(0, len(unmatched_players)-1))
                user1_id = one_league.players[popped_num].id
                user2_id = one_league.players[popped_num2].id

                query = "insert into matchups (week, league_id, user1_id, user2_id) VALUES (%(week)s, %(league_id)s, %(user1_id)s, %(user2_id)s);"
                data = {
                    "week": week,
                    "league_id": id,
                    "user1_id": user1_id,
                    "user2_id": user2_id
                }
                connectToMySQL(DATABASE).query_db( query, data)
                # if there is one player left, they are automatically the winner for that week (i.e. they got a bye)
            if unmatched_players:
                user1_id = one_league.players[unmatched_players[0]]
                query2 = "insert into matchups (week, league_id, user1_id, winner_id) VALUES (%(week)s, %(league_id)s, %(user1_id)s, %(winner_id)s);"
                data2 = {
                    "week": week,
                    "league_id": id,
                    "user1_id": user1_id,
                    "winner_id": user1_id
                }
                connectToMySQL(DATABASE).query_db( query2, data2)
            # increment week to repeat the scheduling process for the next weeks
            week+=1
        return

    # @classmethod
    # def delete(cls, id):
    #     query = "DELETE FROM users WHERE id = %(id)s;"
    #     connectToMySQL(DATABASE).query_db(query, id)
    #     return
