import configparser
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

from servo import move_servo

app = Flask(__name__)
CORS(app)


_FILENAME = "servocam.ini"
_POSITION_KEY = "position"
servo_x_pos = 90
servo_y_pos = 90
servo_locked = False


config = configparser.ConfigParser()


def save_positions(x, y):
    try:
        config[_POSITION_KEY]["x"] = x
        config[_POSITION_KEY]["y"] = y
        with open(_FILENAME, "w") as configfile:
            config.write(configfile)
    except:
        pass


def get_saved_positions():
    _config = config.read(_FILENAME)

    x = servo_x_pos
    y = servo_y_pos

    if _POSITION_KEY in _config:
        x = _config[_POSITION_KEY].getint("x", x)
        y = _config[_POSITION_KEY].getint("y", y)

    return x, y


@app.errorhandler(Exception)
def internal_error(error):
    return jsonify({"success": False, "error": str(error)})


@app.route("/servo", methods=["GET"])
def get_position():
    x, y = get_saved_positions()
    return jsonify({"success": True, "x": x, "y": y})


@app.route("/servo", methods=["POST"])
def update_position():
    global servo_x_pos
    global servo_y_pos
    global servo_locked

    if servo_locked:
        return jsonify({"success": False})

    content = request.get_json()
    axis = content["axis"]
    new_pos = -1

    try:
        direction = content["direction"]
        if axis == "x":
            new_pos = servo_x_pos + int(direction)
        if axis == "y":
            new_pos = servo_y_pos + int(direction)
    except KeyError:
        new_pos = int(content["position"])

    if new_pos < 0:
        new_pos = 0
    if new_pos > 180:
        new_pos = 180

    servo_locked = True
    move_servo(axis, new_pos)

    if axis == "x":
        servo_x_pos = new_pos
    if axis == "y":
        servo_y_pos = new_pos

    save_positions(servo_x_pos, servo_y_pos)

    servo_locked = False

    return jsonify({"success": True})


@app.route("/servo/reset", methods=["POST"])
def reset_potition():
    global servo_x_pos
    global servo_y_pos
    global servo_locked

    if servo_locked:
        return jsonify({"success": False})

    servo_x_pos = 90
    servo_y_pos = 90
    servo_locked = True
    move_servo("x", servo_x_pos)
    move_servo("y", servo_y_pos)
    save_positions(servo_x_pos, servo_y_pos)
    servo_locked = False

    return jsonify({"success": True})


if __name__ == "__main__":
    move_servo("x", servo_x_pos)
    move_servo("y", servo_y_pos)
    app.run(host="0.0.0.0", port=8888)
