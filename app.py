import time

from flask import Flask, jsonify, request
from flask_cors import CORS
from servo import move_servo

app = Flask(__name__)
CORS(app)

servo_x_pos = 90
servo_y_pos = 90
servo_locked = False


@app.route("/servo", methods=["POST"])
def update_position():
    global servo_x_pos
    global servo_y_pos
    global servo_locked

    if servo_locked:
        return jsonify({"success": False})

    content = request.get_json()
    axis = content["axis"]
    direction = content["direction"]

    new_pos = -1
    if axis == "x":
        new_pos = servo_x_pos + int(direction)
    if axis == "y":
        new_pos = servo_y_pos + int(direction)


    if new_pos < 0:
        new_pos = 0
    if new_pos > 180:
        new_pos = 180

    servo_locked = True
    move_servo(axis, new_pos)
    servo_locked = False

    if axis == "x":
        servo_x_pos = new_pos
    if axis == "y":
        servo_y_pos = new_pos

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
    servo_locked = False

    return jsonify({"success": True})


if __name__ == "__main__":
    move_servo("x", servo_x_pos)
    move_servo("y", servo_y_pos)
    app.run(host="0.0.0.0", port=8080)
