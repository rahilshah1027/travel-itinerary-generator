from flask import Flask, url_for, session
from flask import render_template, redirect
from flask_sqlalchemy import SQLAlchemy
#from authlib.integrations.flask_client import OAuth
from sqlalchemy.orm import DeclarativeBase
import os, requests

class Base(DeclarativeBase):
  pass

app = Flask(__name__, template_folder='../client/templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
#oauth = OAuth(app)

GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
# oauth.register(
#     name='google',
#     server_metadata_url=CONF_URL,
#     client_kwargs={
#         'scope': 'openid email profile'
#     }
# )

# creating database models
# class User(db.Model):
#     pass
# class Itinerary(db.Model):
#     pass

# all the routes
# @app.route("/users")
# def user_list():
#     users = db.session.execute(db.select(User).order_by(User.username)).scalars()
#     return render_template("user/list.html", users=users)

@app.route('/')
def homepage():
    #user = session.get('user')
    return render_template('home.html')

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    #return oauth.google.authorize_redirect(redirect_uri)
    pass

@app.route('/auth')
def auth():
    #token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')