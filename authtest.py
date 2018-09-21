import json
from flask import Flask, request, redirect, g, render_template, jsonify
import requests
import base64
import urllib
import spotipy
from spotipy import oauth2
import spotipy.util as util


# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.


app = Flask(__name__)

PORT = 8080
SPOTIPY_CLIENT_ID = "40673f62ed1d44b387160bf9e82a2de1"
SPOTIPY_CLIENT_SECRET = '7a3ee97f8220400e9edf8a3b01fcc84f'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read user-read-playback-state'
CACHE = '.spotipyoauthcache'
SPOTIPY_PLAYLIST_API = "https://api.spotify.com/v1/playlists/{1IAY7B3G3MKO9Pre7cxA9A}/tracks"

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

@app.route('/')
def index():

    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print "Found cached token!"
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print "Found Spotify auth code in Request URL! Trying to get valid access token..."
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print "Access token available! Trying to get user information..."
        sp = spotipy.Spotify(access_token)

        url = SPOTIPY_PLAYLIST_API
        resp = requests.get(url)

        playback= sp.current_playback()
        temp = playback['is_playing']
        playback = 'is a song playing? ' + str(temp)


        tracks = sp.user_playlist_tracks('mitch.s.thomson','23bAhdjxikjjJkDiDuF1zA')
        tracksjson = jsonify(tracks)
        trackarray = []

        for item in tracks['items']:
           trackarray.append([item['track']['name'],item['track']['uri']])

        tempoarray = []

        for track in trackarray:
            audiotrack = str(track[1])
            audiofeat = sp.audio_features(audiotrack)
            tempoarray.append(audiofeat[0]['tempo'])

        durationarray = []

        for track in trackarray:
            audiotrack = str(track[1])
            audiofeat = sp.audio_features(audiotrack)
            durationarray.append(audiofeat[0]['duration_ms'])

        mergearray = []
        i = 0
        mergearray.append(playback)
        for j in tempoarray:
            mergearray.append(trackarray[i])
            mergearray.append(tempoarray[i])
            mergearray.append(durationarray[i])
            i = i + 1


        return jsonify(mergearray)

    else:
        return htmlForLoginButton()

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>You goofed it up</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

if __name__ == "__main__":
    app.run(debug=True,port=PORT)
