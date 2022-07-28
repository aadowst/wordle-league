from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash


from flask_app.models import model_matchup
from flask_app.models.model_score import Score

@app.route('/submitscore', methods=["post"])
def save_score_controller():
    Score.update_score_model(request.form)
    return redirect(f'/matchups/{request.form["matchup_id"]}')

