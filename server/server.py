from flask import Flask, url_for, session
from flask import render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os, requests
from api import fetch_places
from flask import jsonify, request
from dotenv import load_dotenv

app = Flask(__name__, template_folder='../client/templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.secret_key = "randomstuff"
db = SQLAlchemy(app)
oauth = OAuth(app)
load_dotenv()

# creating database models
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
#class Itinerary(db.Model):
    #pass
with app.app_context():
    db.create_all()

GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_SECRET')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    client_id = GOOGLE_CLIENT_ID,
    client_secret = GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)



# all the routes
# @app.route("/users")
# def user_list():
#     users = db.session.execute(db.select(User).order_by(User.username)).scalars()
#     return render_template("user/list.html", users=users)

@app.route('/')
def homepage():
    if 'user' in session:
        user = session['user']
        print("User in session")
    else:
        print("User not in session")
        return redirect(url_for('login'))
    #opentripmap api call
    lat, lon = 40.7128, -74.0060  # Example coordinates
    places_response = fetch_places(lat, lon)
    return render_template('home.html', places=places_response['features'])

#chatgpt chat
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    api_url = "https://api.openai.com/v1/chat/completions"  # This URL might change based on the API you're using
    api_key = 1 #PUT OPENAI API KEY HERE

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
    if 'user' in session:
        return redirect(url_for('/'))
    redirect_uri = url_for('auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
    
def user_create(name, email):
    user = User(
        name=name,
        email=email,
    )
    db.session.add(user)
    db.session.commit()
    print("User Added: ", user)
    return redirect(url_for('/'))

@app.route('/auth')
def auth():
    if 'user' not in session:
        token = oauth.google.authorize_access_token()
        session['user'] = token['userinfo']
        user_info = session['user']
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user_create(user_info['name'], user_info['email'])
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


#opentripmap api call

