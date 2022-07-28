
from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash


from flask_app.models.model_league import League
from flask_app.models import model_matchup


@app.route('/joinleaguebyid', methods=["post"])
def controller_join_league():
    League.model_join_league(request.form)
    id = request.form["league_id"]
    return redirect(f'/oneleague/{id}')

@app.route('/moreleagues')
def moreleagues():
    not_my_leagues = League.get_not_my_leagues({"user_id": session['user_id']})
    return render_template("moreleagues.html", not_my_leagues=not_my_leagues)


@app.route('/createleague', methods=["post"])
def createleague():
    League.save(request.form)
    return redirect('/oneleague')

@app.route('/selectleague', methods=['post'])
def viewonselect():
    print(request.form)
    id = request.form['league_id']

    return redirect(f'/oneleague/{id}')

@app.route('/oneleague/<int:id>/')
@app.route('/oneleague/<int:id>/<int:week>')
def viewleague(id, week=1):
    matchups = model_matchup.Matchup.view_league_matchups({"league_id": id, "week": week})
    print("matchups is:  ", matchups)
    one_league = League.get_league_with_players({"id": id})
    return render_template("oneleague.html", one_league=one_league, matchups=matchups)
# Create Display NOT NEEDED
# @app.route('/users/new')
# def new():
#     return render_template("create.html")

# Read 

@app.route('/createschedule/<int:id>')
def create_schedule_controller(id):
    League.create_schedule(id)
    return redirect(f'/oneleague/{id}')


# ***********************************UPDATE TO GO HERE ******************************************

@app.route('/oneleague/update', methods=["post"])
def update_league_controller():
    League.update_league_model(request.form)
    id = request.form["id"]
    return redirect(f'/oneleague/{id}')

# ************************************DELETE TO GO HERE*****************************************

