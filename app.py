from flask import Flask
from yeelight import *
import funktionen

app = Flask(__name__)

ip = None
bulbs = discover_bulbs()
ip = bulbs[0]['ip']



#Code Party function

#@app.route ("/beatspm")







#@app.route ("/")





#Basic functions


@app.route("/on")
def on():
    return funktionen.on(ip)

@app.route("/off")
def off():
    return funktionen.off(ip)

@app.route("/flow")
def flow():
    return funktionen.flow(ip)

@app.route("/brightness")
def brightness():
    return funktionen.brightness(ip,10)

@app.route("/red")
def red():
    return funktionen.red(ip)


@app.route("/mode1")
def mode1():
    return funktionen.mode1(ip)






