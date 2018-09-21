import json
from flask import Flask, request, redirect, g, render_template, jsonify
import requests
import base64
import urllib
import spotipy
from spotipy import oauth2
import spotipy.util as util

app = Flask(__name__)

PORT = 8080
SPOTIPY_CLIENT_ID = "40673f62ed1d44b387160bf9e82a2de1"
SPOTIPY_CLIENT_SECRET = '7a3ee97f8220400e9edf8a3b01fcc84f'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read user-read-playback-state'
CACHE = '.spotipyoauthcache'
SPOTIPY_PLAYLIST_API = "https://api.spotify.com/v1/playlists/{1IAY7B3G3MKO9Pre7cxA9A}/tracks"

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

access_token = 'BQAUGpBXq-MWnOUJJJ1uT6uZoDU_WB3x3qyAu1-cBR_efutOOqsmJR-4LNGbTuOX1sLoHgyXbzRZ2y7BkmXJ4968fAPzT-AYnidvHkBKXgR5xxQonkgfGp30nWpEZy60sR74JGabOuE0YAPsNU3ziRGYvjtuKtv9WXXuO6gK20HHMv1wE71nsBEdhGL5UZPdnr3QNg'
sp = spotipy.Spotify(access_token)

url = SPOTIPY_PLAYLIST_API
resp = requests.get(url)

playback= sp.current_playback()
isplaying = playback['is_playing']
songid = playback['item']['uri']
result = []
result.append(isplaying)
result.append(songid)

song = []
song = str(songid)
playing = []
playing = isplaying

tempo = 0

audiofeat = sp.audio_features(song)
tempo = (audiofeat[0]['tempo'])

duration = 0

audiofeat = sp.audio_features(song)
duration= (audiofeat[0]['duration_ms'])

merge = []
merge.append(playing)
merge.append(tempo)
merge.append(duration)
merge.append(song)


@app.route('/')
def index():
    print "It is running"
    return jsonify(merge)
    
if __name__ == "__main__":
    app.run(debug=True,port=PORT)
