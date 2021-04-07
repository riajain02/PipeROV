#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, request, Response
import atexit
import time
import RPi.GPIO as GPIO
import os
from mygps import mygps_get_coordinates
from mycompass import mycompass_get_heading
from mycar import mycar_drive, mycar_turn, mycar_stop
Camera = import_module('camera_pi').Camera

socketFlagFile = os.getenv('HOME') + '/_tmp_socketmode'
if os.path.isfile(socketFlagFile) == True: os.remove(socketFlagFile)
socketmode  = 0

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/stream')
def stream():
    def get_message():
        '''this could be any function that blocks until data is ready'''
        time.sleep(1.0)
        s = time.ctime(time.time())
        return s
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/api/stream2')
def stream2():
    def get_message2():
        '''this could be any function that blocks until data is ready'''
        time.sleep(1.0)
        lat_in_degrees, long_in_degrees = mygps_get_coordinates()
        heading = mycompass_get_heading()
        s = "LAT: %s deg, LONG: %s deg, DIR: %s deg\n\n" % (lat_in_degrees, long_in_degrees, heading)
        return s
    def eventStream2():
        while True:
            yield 'data: {}\n\n'.format(get_message2())
    return Response(eventStream2(), mimetype="text/event-stream")

@app.route('/drive', methods=['POST'])
def route_drive():
    '''
    Listen for POST requests to /drive and process them
    '''
    if socketmode == 0: mycar_drive(float(request.form['value']))
    return 'Drive'

@app.route('/turn', methods=['POST'])
def route_turn():
    '''
    Listen for POST requests to /turn and process them
    '''
    if socketmode == 0: mycar_turn(float(request.form['value']))
    return 'Turn'

@app.route('/stop', methods=['POST'])
def route_stop():
    '''
    Listen for POST requests to /stop and process them
    '''
    if socketmode == 0: mycar_stop()
    return 'Stop'

@app.route('/socketmode', methods=['POST'])
def route_socketmode():
    '''
    Listen for POST requests to /socketmode and process them
    '''
    global socketmode 
    socketmode = float(request.form['value'])
    if (socketmode == 1): 
        fo = open(socketFlagFile, "w")
        fo.close()
    else:
        os.remove(socketFlagFile)
    return 'SocketMode'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True) # run Flask app, threaded allows multiple requests to be handled at once

@atexit.register
def cleanup():
    '''
    Cleans up GPIO pins when app is closed
    '''
    GPIO.cleanup()
