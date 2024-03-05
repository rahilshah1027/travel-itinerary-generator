from flask import Flask, url_for, session
from flask import render_template, redirect
from flask_sqlalchemy import SQLAlchemy
#from authlib.integrations.flask_client import OAuth
from sqlalchemy.orm import DeclarativeBase
import os, requests
from api import fetch_places
from flask import jsonify, request
from dotenv import load_dotenv
import openai


class Base(DeclarativeBase):
  pass

app = Flask(__name__, template_folder='../client/templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
load_dotenv()
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

    #opentripmap api call
    lat, lon = 40.7128, -74.0060  # Example coordinates
    places_response = fetch_places(lat, lon)

    return render_template('home.html', places=places_response['features'])

#chatgpt chat
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    api_url = "https://api.openai.com/v1/chat/completions"  # This URL might change based on the API you're using
    api_key = os.getenv('OPENAI_API_KEY')

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-3.5-turbo",  # Adjust model as needed
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        chat_response = response.json()['choices'][0]['message']['content']
        return jsonify({"response": chat_response})
    else:
        return jsonify({"error": "Failed to fetch response from the API"}), 500

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


#opentripmap api call

