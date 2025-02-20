import spotipy
import os
import json
import time

from flask import Flask, jsonify, redirect, request, session, render_template
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='user-library-read user-top-read' # Modify scope as needed later
)

@app.route('/')
def home():
    try:
        token_info = session.get('token_info', None)
        if not token_info:
            return redirect('/auth')
            # TO-DO :: error handling in case user is not authenticated, issues fetching data from spotipy/Spotify API
        
        if token_expired(token_info):  # Define is_token_expired() elsewhere
            return redirect('/auth')

        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_info = sp.current_user()
        top_tracks = sp.current_user_top_tracks(limit=5)

        print("user info", json.dumps(user_info, indent=4))
        print("tracks", json.dumps(top_tracks, indent=4) )

        # return jsonify(user_info=user_info, top_tracks=top_tracks)
        return render_template('dash.html', user_info=user_info, top_tracks=top_tracks['items'])
    except Exception as e:
        return "Error sorry" # fix later too lazy now

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


def token_expired(t):
    return t['expires_at'] < int(time.time())

app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

if __name__ == '__main__':
    app.run(debug=True)

