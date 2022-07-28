# __init__.py
from flask import Flask, session
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)