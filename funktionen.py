from flask import jsonify
from yeelight import *
import time


def checkIp():
    ip = None
    bulbs = discover_bulbs()
    ip = bulbs[0]['ip']

    if ip is None:
        return False
    else:
        return True

def on(ip):
    if not checkIp():
        return jsonify({'status': 'error', 'message': 'no bulb found'})

    bulb = Bulb(ip)

    try:
       bulb.turn_on()
    except:
       return jsonify({'status': 'error', 'message': 'could not turn on bulb'})

    return jsonify({'status': 'OK'})



def flow(ip):
    if not checkIp():
        return jsonify({'status': 'error', 'message': 'no bulb found'})

    bulb = Bulb(ip)

    transitions = [
        TemperatureTransition(1700, duration=1000),
        SleepTransition(duration=1000),
        TemperatureTransition(6500, duration=1000)
    ]

    flow = Flow(
        count=2,
        action=Flow.actions.recover,
        transitions=transitions
    )

    try:
        bulb.start_flow(flow)


    except:
        return jsonify({'status': 'error', 'message': 'could not adjust brightness'})

    return jsonify({'status': 'OK'})




def off(ip):
    if not checkIp():
        return jsonify({'status': 'error', 'message': 'no bulb found'})


    bulb = Bulb(ip)

    try:
        bulb.turn_off()
    except:
        return jsonify({'status': 'error', 'message': 'could not turn off bulb'})

    return jsonify({'status': 'OK'})



def brightness(ip, brightness):
    if not checkIp():
        return jsonify({'status': 'error', 'message': 'no bulb found'})

    bulb = Bulb(ip)

    try:
        bulb.set_brightness(brightness)

    except:
        return jsonify({'status': 'error', 'message': 'could not adjust brightness'})

    return jsonify({'status': 'OK'})





def red(ip):
    if not checkIp():
        return jsonify({'status': 'error', 'message': 'no bulb found'})

    bulb = Bulb(ip)

    try:

        bulb.set_rgb(255, 0, 0)


    except:
        return jsonify({'status': 'error', 'message': 'could not adjust brightness'})

    return jsonify({'status': 'OK'})



def mode1(ip):
    if not checkIp():
        return jsonify({'status': 'error', 'message': 'no bulb found'})

    for i in range(10):
        funktionen.on(ip)
        off(ip)
        time.sleep(4)

    return jsonify({'status': 'OK'})




def party():
 if not checkIp():
    return jsonify({'status': 'error', 'message': 'no bulb found'})

 for i in range(10):
    funktionen.on(ip)
    funktionen.flow(ip)
    time.sleep(4)
    funktionen.off(ip)
    time.sleep(4)

    return jsonify({'status': 'OK'})











def disco(bpm=120):


    if not checkIp():

        return jsonify({'status': 'error', 'message': 'no bulb found'})




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


