from flask import Flask
from flask import jsonify
from yeelight import Bulb, discover_bulbs
from yeelight import flow
from yeelight import *
import requests
#import random


#from .utils import _clamp

#import base64
#import urllib
import spotipy
from spotipy import oauth2
#import spotipy.util as util
#import json

app = Flask(__name__)

ip = None
bulbs = discover_bulbs()
print(bulbs)
ip = bulbs[0]['ip']


PORT = 8080
SPOTIPY_CLIENT_ID = "40673f62ed1d44b387160bf9e82a2de1"
SPOTIPY_CLIENT_SECRET = '7a3ee97f8220400e9edf8a3b01fcc84f'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read user-read-playback-state'
CACHE = '.spotipyoauthcache'
SPOTIPY_PLAYLIST_API = "https://api.spotify.com/v1/playlists/{1IAY7B3G3MKO9Pre7cxA9A}/tracks"

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SCOPE,
                               cache_path=CACHE)

access_token = 'BQDHm4Ha0AS1P_5l18qhSPXYftU2RHZC_K7gn54PG9PZ0fCvcdjFtj3mZH_RZD-wJfuohHfa4La6yvX4qWkm_A507jrLU3I9BDK_b829HjOyyAy-6YlsK52C3dCkmlS3o5iv_jHi3PgGV6x55SLy5lCJ342PYZA6T10e8tXtIgr9OKbn6AtMrlhbJgp6Eqp7Vgeyag'
sp = spotipy.Spotify(access_token)

url = SPOTIPY_PLAYLIST_API
resp = requests.get(url)

playback = sp.current_playback()
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
duration = (audiofeat[0]['duration_ms'])

merge = []
merge.append(playing)
merge.append(tempo)
merge.append(duration)
merge.append(song)

@app.route('/')
def index():
    print
    "It is running"
    return jsonify(merge)

@app.route("/on")
def on():

   if ip is None:
      return jsonify({'status': 'error', 'message': 'no bulb found'})

   bulb = Bulb(ip)

   try:
      bulb.turn_on()
   except:
      return jsonify({'status': 'error', 'message': 'could not turn on bulb'})

   return jsonify({'status': 'OK'})

@app.route("/off")
def off():

  if ip is None:
      return jsonify({'status': 'error', 'message': 'no bulb found'})

  bulb = Bulb(ip)

  try:
      bulb.turn_off()
  except:
      return jsonify({'status': 'error', 'message': 'could not turn off bulb'})

  return jsonify({'status': 'OK'})

@app.route("/brightness")
def brightness():

   if ip is None:
       return jsonify({'status': 'error', 'message': 'no bulb found'})

   bulb = Bulb(ip)

   try:
       bulb.set_brightness(10)

   except:
       return jsonify({'status': 'error', 'message': 'could not adjust brightness'})


   return jsonify({'status': 'OK'})


@app.route("/party")
def party():

   if ip is None:
       return jsonify({'status': 'error', 'message': 'no bulb found'})

   bulb = Bulb(ip)

   try:

       bulb.set_rgb(255, 0, 0)


   except:
       return jsonify({'status': 'error', 'message': 'could not adjust brightness'})

   return jsonify({'status': 'OK'})

@app.route("/disco")

def disco(bpm = tempo):
    """
    Color changes to the beat.

    :param int bpm: The beats per minute to pulse to.

    :returns: A list of transitions.
    :rtype: list
    """
    duration = int(60000 / bpm)
    transitions = [
        HSVTransition(0, 100, duration=duration, brightness=100),
        HSVTransition(0, 100, duration=duration, brightness=1),
        HSVTransition(90, 100, duration=duration, brightness=100),
        HSVTransition(90, 100, duration=duration, brightness=1),
        HSVTransition(180, 100, duration=duration, brightness=100),
        HSVTransition(180, 100, duration=duration, brightness=1),
        HSVTransition(270, 100, duration=duration, brightness=100),
        HSVTransition(270, 100, duration=duration, brightness=1),
    ]
    bulb = Bulb(ip)
    flow = Flow(
        count=0,  # Cycle forever.
        transitions=transitions
    )

    bulb.start_flow(flow)

    return jsonify({'status': 'OK'})


if __name__ == "__main__":
    app.run(debug=True, port=PORT)