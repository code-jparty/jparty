from flask import Flask
from yeelight import *
rom flask import jsonify
from yeelight import *
import time
import random

from .flow import HSVTransition, RGBTransition, SleepTransition, TemperatureTransition
from .utils import _clamp
from yeelight import Bulb, discover_bulbs
app = Flask(__name__)



ip = None
bulbs = discover_bulbs()
ip = bulbs[0]['ip']




@app.route.(/"disco")

def disco (ip, 120):


    if ip is None:
        return jsonify({'status': 'error', 'message': 'no bulb found'})

    bulb = Bulb(ip)


  try.bulb.


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
    return transitions














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