
from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash


from flask_app.models.model_user import User


# Create Action 
@app.route('/register', methods=["POST"])
def register():

    if not User.validate_registration(request.form):
        return redirect ('/')
    password_hash = bcrypt.generate_password_hash(request.form['password'])

    # put the pw_hash into the data dictionary
    data = {
        **request.form,
        'password': password_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form["first_name"]
    return redirect('/dashboard')


# Create Display NOT NEEDED
# @app.route('/users/new')
# def new():
#     return render_template("create.html")

# Read 


@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.email_match(data)
    print(user_in_db)
    if not user_in_db:
        flash("invalid email or password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid email or password", "login")
        return redirect('/')
    session['first_name'] = user_in_db.first_name
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')





# @app.route('/success/<int:id>')
# def read_one_commment(id):
#     email = User.get_one({"id": id})
#     all_emails = User.get_all()
#     return render_template("result.html", email=email, all_emails=all_emails)

# @app.route('/delete', methods=["POST"])
# def delete_email():
#     id = request.form["id"]
#     print("id is:  ", id)
#     print("request.form id is: ", request.form["id"])
#     User.delete(request.form)
#     return redirect('/')
    


# ***********************************UPDATE TO GO HERE ******************************************

# ************************************DELETE TO GO HERE*****************************************

