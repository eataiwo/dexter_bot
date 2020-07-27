from flask import Flask, render_template, redirect, url_for, make_response, Response
import socket

from src.powertrain.powertrain import Powertrain
from src.camera.camera import Camera

direction_pins = (27, 23, 19, 20)
step_pins = (22, 24, 26, 21)

dexter = Powertrain(direction_pins, step_pins)
dexter.setup()

# Get server ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', server_ip=server_ip)


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changepin = int(changepin)
    if changepin == 1:
        dexter.remote_direction = 'left'
    elif changepin == 2:
        dexter.remote_direction = 'forward'
    elif changepin == 3:
        dexter.remote_direction = 'right'
    elif changepin == 4:
        dexter.remote_direction = 'backward'
    elif changepin == 5:
        dexter.stop()
    elif changepin == 6:
        dexter.remote_direction = 'tots_cw'
    elif changepin == 7:
        dexter.remote_direction = 'tots_ccw'
    elif changepin == 8:
        dexter.speed -= 5
    elif changepin == 9:
        dexter.speed += 5
    else:
        print("Wrong command")

    if not dexter.drive and changepin != 5:  # or changepin == 8 or changepin == 9:

        # Move dexter with the new powertrain variables
        dexter.remote_control()

    response = make_response(redirect(url_for('index')))
    return response


app.run(debug=True, host='0.0.0.0', port=8000)