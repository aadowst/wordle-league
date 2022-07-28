
from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash


from flask_app.models import model_score
from flask_app.models.model_matchup import Matchup

@app.route('/matchups/<int:id>')
def showmatchup(id):
    one_matchup = Matchup.view_one_matchup({"id": id})
    data1 = {
        "user_id": one_matchup.players[0].id,
        "week": one_matchup.week
    }
    player1_scores = model_score.Score.get_player_scores(data1)

    data2 = {
        "user_id": one_matchup.players[1].id,
        "week": one_matchup.week
    }
    player2_scores = model_score.Score.get_player_scores(data2)

    updateboxscorecontroller(one_matchup, player1_scores, player2_scores)

    return render_template("onematchup.html", one_matchup=one_matchup, player1_scores=player1_scores, player2_scores=player2_scores)


@app.route('/updateboxscore')
def updateboxscorecontroller(one_matchup, player1_scores, player2_scores):
    Matchup.updateboxscore_model(one_matchup, player1_scores, player2_scores)
    return