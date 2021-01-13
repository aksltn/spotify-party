from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
import json
import urllib.request
import urllib.parse

config_file = f'{os.path.dirname(os.path.abspath(__file__))}/config.json'

with open(config_file, 'r') as f:
    config = json.load(f)

SPOTIFY_CLIENT_ID = config['client_id']
SPOTIFY_CLIENT_SECRET = config['client_secret']

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL = "https://api.spotify.com/v1"

CLIENT_SIDE_URL = 'http://127.0.0.1'
PORT = 5000
SPOTIFY_REDIRECT_URI = f"{CLIENT_SIDE_URL}:{PORT}/callback/q"
SPOTIFY_SCOPE = 'playlist-read-private playlist-read-collaborative'

spotify_auth_query_parameters = {
    'client_id': SPOTIFY_CLIENT_ID,
    'response_type': 'code',
    'redirect_uri': SPOTIFY_REDIRECT_URI,
    'scope': SPOTIFY_SCOPE,
}

app = Flask(__name__)
app.secret_key = os.urandom(32)


def spotify_api_query(url, method):
    authorization_header = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    req = urllib.request.Request(
        url,
        headers=authorization_header,
        method=method,
    )
    req = urllib.request.urlopen(req)

    if method == 'GET':
        res = req.read()
        data = json.loads(res)
        return data
    return None


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/connect')
def connect():
    url_args = "&".join([f"{key}={urllib.parse.quote(val)}" for key,
                         val in spotify_auth_query_parameters.items()])
    auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"
    return redirect(auth_url)


@app.route('/callback/q')
def callback():
    auth_token = request.args['code']
    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }

    post_request = urllib.request.Request(
        SPOTIFY_TOKEN_URL,
        data=urllib.parse.urlencode(code_payload).encode()
    )

    post_request = urllib.request.urlopen(post_request)
    post_request = post_request.read()

    response_data = json.loads(post_request)
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    token_type = response_data['token_type']
    expires_in = response_data['expires_in']

    session['access_token'] = access_token

    return redirect(url_for('root'))


if __name__ == "__main__":
    app.run(debug=True)
