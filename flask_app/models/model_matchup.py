

DATABASE = "wordle_league"

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import model_user


class Matchup:
    def __init__( self , data ):

        self.id = data['id']
        self.week = data['week']
        self.league_id = data['league_id']
        self.user1_id = data['user1_id']
        self.user2_id = data['user2_id']
        self.players = []


    @classmethod
    def view_league_matchups(cls, data):

        query = "SELECT * FROM users join matchups on users.id = matchups.user1_id join users as users2 on matchups.user2_id = users2.id where matchups.league_id = %(league_id)s and week = %(week)s;"

        # will need to add week number to the query
        results = connectToMySQL(DATABASE).query_db(query, data)

        all_matchups = []
        for row_from_db in results:

            matchup = cls(row_from_db)
            entry = {
                "id": row_from_db["id"],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "email": row_from_db["email"],
                "password": row_from_db['password'],
                "created_at": row_from_db['created_at'],
                "updated_at": row_from_db['updated_at']
            }

            player1 = model_user.User(entry)

            matchup.players.append(player1)

            entry2 = {
                "id": row_from_db["users2.id"],
                "first_name": row_from_db["users2.first_name"],
                "last_name": row_from_db["users2.last_name"],
                "email": row_from_db["users2.email"],
                "password": row_from_db['users2.password'],
                "created_at": row_from_db['users2.created_at'],
                "updated_at": row_from_db['users2.updated_at']
            }

            player2 = model_user.User(entry2)
            matchup.players.append(player2)
            matchup.matchup_id = row_from_db["matchups.id"]
            all_matchups.append(matchup)
        return all_matchups


    @classmethod
    def view_one_matchup(cls, data):

        query = "SELECT * FROM users join matchups on users.id = matchups.user1_id join users as users2 on matchups.user2_id = users2.id where matchups.id = %(id)s"

        # will need to add week number to the query
        results = connectToMySQL(DATABASE).query_db(query, data)

        one_matchup = []
        for row_from_db in results:
            matchup = cls(row_from_db)
            matchup.id = data["id"]

            entry = {
                "id": row_from_db["id"],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "email": row_from_db["email"],
                "password": row_from_db['password'],
                "created_at": row_from_db['created_at'],
                "updated_at": row_from_db['updated_at']
            }
            player1 = model_user.User(entry)
            matchup.players.append(player1)

            entry2 = {
                "id": row_from_db["users2.id"],
                "first_name": row_from_db["users2.first_name"],
                "last_name": row_from_db["users2.last_name"],
                "email": row_from_db["users2.email"],
                "password": row_from_db['users2.password'],
                "created_at": row_from_db['users2.created_at'],
                "updated_at": row_from_db['users2.updated_at']
            }
            player2 = model_user.User(entry2)
            matchup.players.append(player2)
            one_matchup.append(matchup)

    
        return one_matchup[0]

    @classmethod
    def updateboxscore_model(cls,one_matchup, player1_scores, player2_scores):
        user1_score = 0
        user2_score = 0

        if(not player1_scores and not player2_scores):
            return
        elif(player1_scores and not player2_scores):
            winner_id = one_matchup.players[0].id
            loser_id = one_matchup.players[1].id
        elif(player2_scores and not player1_scores):
            winner_id = one_matchup.players[1].id
            loser_id = one_matchup.players[0].id
        else:
            for x in range(1,6):
                if (not player1_scores[f"day{x}"] or not player2_scores[f"day{x}"]):
                    break
                else:
                    if (player1_scores[f"day{x}"] < player2_scores[f"day{x}"]):
                        user1_score +=3
                    elif (player1_scores[f"day{x}"] > player2_scores[f"day{x}"]):
                        user2_score +=3
                    elif (player1_scores[f"day{x}"] == player2_scores[f"day{x}"]):
                        user1_score +=1
                        user2_score +=1

            if user1_score > user2_score:
                winner_id = one_matchup.players[0].id
                loser_id = one_matchup.players[1].id
            elif user1_score < user2_score:
                winner_id = one_matchup.players[1].id
                loser_id = one_matchup.players[0].id
                # if there is a tie, then the total number of guesses for the week are compared to determine a winner
            else:
                user1_total =0
                user2_total = 0
                for y in range(1,6):
                    if player1_scores[f"day{y}"]:
                        user1_total += int(player1_scores[f"day{y}"])
                    if player2_scores[f"day{y}"]:
                        user2_total += int(player2_scores[f"day{y}"])

                if user1_total < user2_total:
                    winner_id = one_matchup.players[0].id
                    loser_id = one_matchup.players[1].id
                elif user1_total > user2_total:
                    winner_id = one_matchup.players[1].id
                    loser_id = one_matchup.players[0].id
                # if there is still a tie, then user1 wins due to 'homefield advantage' This could be modified in the future to other tie breakers
                else:
                    winner_id = one_matchup.players[0].id
                    loser_id = one_matchup.players[1].id

            dict = {
                "week": one_matchup.week,
                "league_id": one_matchup.league_id,
                "user1_id": one_matchup.players[0].id,
                "user2_id": one_matchup.players[1].id,
                "winner_id": winner_id,
                "loser_id": loser_id
            }


            query = "UPDATE matchups SET winner_id = %(winner_id)s, loser_id = %(loser_id)s where user1_id = %(user1_id)s and week = %(week)s and league_id = %(league_id)s;"
            return connectToMySQL(DATABASE).query_db( query, dict )


#  @classmethod  ORIGINAL
#     def updateboxscore_model(cls,one_matchup, player1_scores, player2_scores):
#         user1_score = 0
#         user2_score = 0
#         if (not player1_scores or not player2_scores):
#             return
#         else:
#             if (player1_scores['day1'] < player2_scores['day1']):
#                 user1_score +=3
#             elif (player1_scores['day1'] > player2_scores['day1']):
#                 user2_score +=3
#             elif (player1_scores['day1'] == player2_scores['day1']):
#                 user1_score +=1
#                 user2_score +=1

#             if (player1_scores['day2'] < player2_scores['day2']):
#                 user1_score +=3
#             elif (player1_scores['day2'] > player2_scores['day2']):
#                 user2_score +=3
#             elif (player1_scores['day2'] == player2_scores['day2']):
#                 user1_score +=1
#                 user2_score +=1

#             if (player1_scores['day3'] < player2_scores['day3']):
#                 user1_score +=3
#             elif (player1_scores['day3'] > player2_scores['day3']):
#                 user2_score +=3
#             elif (player1_scores['day3'] == player2_scores['day3']):
#                 user1_score +=1
#                 user2_score +=1

#             if (player1_scores['day4'] < player2_scores['day4']):
#                 user1_score +=3
#             elif (player1_scores['day4'] > player2_scores['day4']):
#                 user2_score +=3
#             elif (player1_scores['day4'] == player2_scores['day4']):
#                 user1_score +=1
#                 user2_score +=1

#             if (player1_scores['day5'] < player2_scores['day5']):
#                 user1_score +=3
#             elif (player1_scores['day5'] > player2_scores['day5']):
#                 user2_score +=3
#             elif (player1_scores['day5'] == player2_scores['day5']):
#                 user1_score +=1
#                 user2_score +=1

#             print("11111111111111111111111111111111111111111111111111111", user1_score)
#             print("222222222222222222222222222222222222222222222222222222", user2_score)
#             if user1_score > user2_score:
#                 winner_id = one_matchup.players[0].id
#                 loser_id = one_matchup.players[1].id
#             elif user1_score < user2_score:
#                 winner_id = one_matchup.players[1].id
#                 loser_id = one_matchup.players[0].id
#                 # if there is a tie, then the total number of guesses for the week are compared to determine a winner
#             else:
#                 user1_total =0
#                 user2_total = 0
#                 for x in player1_scores:
#                     user1_total += int(player1_scores[x])
#                 for y in player2_scores:
#                     user2_total += int(player1_scores[y])
#                 if user1_total < user2_total:
#                     winner_id = one_matchup.players[0].id
#                     loser_id = one_matchup.players[1].id
#                 elif user1_total > user2_total:
#                     winner_id = one_matchup.players[1].id
#                     loser_id = one_matchup.players[0].id
#                 # if there is still a tie, then user1 wins due to 'homefield advantage' This could be modified in the future to other tie breakers
#                 else:
#                     winner_id = one_matchup.players[0].id
#                     loser_id = one_matchup.players[1].id

#             dict = {
#                 "week": one_matchup.week,
#                 "league_id": one_matchup.league_id,
#                 "user1_id": one_matchup.players[0].id,
#                 "user2_id": one_matchup.players[1].id,
#                 "winner_id": winner_id,
#                 "loser_id": loser_id
#             }


#             query = "UPDATE matchups SET winner_id = %(winner_id)s, loser_id = %(loser_id)s where user1_id = %(user1_id)s and week = %(week)s and league_id = %(league_id)s;"
#             return connectToMySQL(DATABASE).query_db( query, dict )

    # @classmethod
    # def view_league_matchups(cls, data):
    #     print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    #     query = "SELECT * FROM users join matchups on users.id = matchups.user1_id join users as users2 on matchups.user2_id = users2.id where matchups.league_id = %(league_id)s"
    #     results = connectToMySQL(DATABASE).query_db(query, data)

    #     all_matchups = []
    #     for row_from_db in results:
    #         print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR",row_from_db)
    #         entry = {
    #             "id": row_from_db["id"],
    #             "first_name": row_from_db["first_name"],
    #             "last_name": row_from_db["last_name"],
    #             "email": row_from_db["email"],
    #             "password": row_from_db['password'],
    #             "created_at": row_from_db['created_at'],
    #             "updated_at": row_from_db['updated_at']
    #         }
    #         print("entry is:  ",entry)
    #         player = model_user.User(entry)
            
    #         all_matchups.append(player)

    
    #     return all_matchups