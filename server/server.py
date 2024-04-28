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
        return render_template('login.html')

    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    interests = request.form.getlist('interests')
    # check if the user entered any interests
    if len(interests) == 0:
        error = "Please select an interest"
        return render_template("results.html", error=error)
    
    locations = {
        'nature': 'New York City might seem like an unlikely destination for nature lovers, but it surprisingly offers numerous green spaces and natural retreats. Central Park, the citys most iconic park, spans over 840 acres and features meadows, woodlands, lakes, and gardens.',
        'sports': 'If you are interested in sports, you should check out New York City! From the US Open Tennis Championships to major league games (MLB, NBA, NFL), NYC is a sports melting pot. Additionally, the city hosts the New York Marathon.',
        'historical': 'New York City is a treasure trove for history enthusiasts for several reasons, encompassing a broad range of historical periods and cultural developments. This includes American Immigrant history, the American Revolutionary War, and the history of Wall Street.',
        'architecture': 'add something here',
        'amusements': 'add something here'
        # Add more interests and locations as needed
    }
    selected_locations = [locations[interest] for interest in interests if interest in locations]

    interest_map = {
        'nature': 'natural',
        'sports': 'sport',
        'historical': 'historic',
        'architecture': 'architecture',
        'amusements': 'amusements',
        # Add more interests and locations as needed
    }
    kinds = ','.join(interest_map[i] for i in interests if i in interest_map)

    #opentripmap api call
    #interests = request.form.getlist('interests')
    lat, lon = 40.7128, -74.0060
    places_response = fetch_places(lat, lon, kinds=kinds)
    print(places_response['features'])
    places = [places_response['features'][i] for i in range(5)]
    print(places)
    return render_template('results.html', interests=interests, selected_locations=selected_locations, places=places)

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

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
