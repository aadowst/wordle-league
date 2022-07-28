# Name of Assignment 
from flask_app import app
from flask_app.controllers import controller_route, controller_user, controller_league, controller_matchup, controller_score


if __name__ == "__main__":
    app.run(debug=True)