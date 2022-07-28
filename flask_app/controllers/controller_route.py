from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash

from flask_app.models.model_league import League
from flask_app.models.model_user import User


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    my_leagues = League.get_my_leagues({"user_id": session['user_id']})
    user_info = User.get_one_user({"id": session['user_id']})
    return render_template("dashboard.html", user_info=user_info, my_leagues=my_leagues)

@app.route('/logout', methods=["get", 'POST'])
def logout():
    del session["user_id"]
    del session["first_name"]
    return redirect ('/')