from flask import Flask, jsonify, redirect, request, session
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import os
# Flask for building webapp
# jsonify converts Python dict -> JSON format (API handling)
# redirect redirects, request accesses request data (query parameters) to handle callback, session stores users authentication token
# load_dotenv loads environment variables (and os needed to interact with operating system, specifically in this case to read .env)

app = Flask(__name__)
load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-top-read" # Modify scope as needed later
)

@app.route('/')
def home():
    return jsonify(message="test")
    # returns JSON response (instead of HTML), used for API endpoints

@app.route('/auth')
def authenticate():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# After user logs in, Spotify redirects to callback
@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code']) # retrieve access token
    session['token_info'] = token_info # store access token in session
    return redirect('/')


app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

if __name__ == '__main__':
    app.run(debug=True)

