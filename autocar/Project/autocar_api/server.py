# server.py
"""
Autocar 내부에서 실행하는 Flask API 서버입니다.

실행:
    python3 server.py
    python3 server.py --real

주요 API:
    GET  /api/status
    POST /api/motor
    POST /api/steering
    POST /api/drive
    POST /api/camera/pan_tilt
    POST /api/camera/start
    POST /api/camera/stop
    GET  /video_feed
    POST /api/sound/tone
    POST /api/sound/tts
    POST /api/stop
"""

import argparse
import time
import threading

from flask import Flask, Response, jsonify, request

import config
from car_controller import MockCarController, RealCarController
from camera_controller import CameraStream, MockCameraPanTilt, RealCameraPanTilt
from sound_controller import MockSoundController, RealSoundController


app = Flask(__name__)

state_lock = threading.Lock()

server_state = {
    "server": "running",
    "mode": "mock",
    "last_error": "",
    "last_drive_time": 0.0,
}

car = None
camera_stream = None
camera_pan_tilt = None
sound = None


def make_error(message, status_code=400):
    with state_lock:
        server_state["last_error"] = str(message)

    return jsonify({
        "ok": False,
        "error": str(message),
    }), status_code


def parse_json_body():
    data = request.get_json(silent=True)

    if data is None:
        raise ValueError("JSON body가 필요합니다.")

    return data


def get_number(data, key):
    if key not in data:
        raise ValueError(f"'{key}' 값이 필요합니다.")

    try:
        return float(data[key])
    except (TypeError, ValueError):
        raise ValueError(f"'{key}' 값은 숫자여야 합니다.")


def validate_range(value, min_value, max_value, name):
    if value < min_value or value > max_value:
        raise ValueError(f"'{name}' 범위는 {min_value} ~ {max_value} 입니다.")

    return value


@app.after_request
def add_cors_headers(response):
    """
    노트북 pywebview 대시보드에서 fetch로 Autocar API에 접근할 수 있도록 CORS 헤더를 추가합니다.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "ok": True,
        "message": "Autocar API server is running",
        "endpoints": {
            "status": "GET /api/status",
            "motor": "POST /api/motor",
            "steering": "POST /api/steering",
            "drive": "POST /api/drive",
            "camera_pan_tilt": "POST /api/camera/pan_tilt",
            "camera_start": "POST /api/camera/start",
            "camera_stop": "POST /api/camera/stop",
            "video_feed": "GET /video_feed",
            "tone": "POST /api/sound/tone",
            "tts": "POST /api/sound/tts",
            "stop": "POST /api/stop",
        },
    })


@app.route("/api/status", methods=["GET"])
def api_status():
    with state_lock:
        data = dict(server_state)

    data.update({
        "ok": True,
        "car": car.get_status(),
        "camera": {
            "stream": camera_stream.get_status(),
            "pan_tilt": camera_pan_tilt.get_status(),
        },
        "sound": sound.get_status(),
        "limits": {
            "motor_speed": [-100, 100],
            "applied_max_speed": config.MAX_SPEED,
            "steering_angle": [config.MIN_STEERING_ANGLE, config.MAX_STEERING_ANGLE],
            "pan": [config.MIN_PAN, config.MAX_PAN],
            "tilt": [config.MIN_TILT, config.MAX_TILT],
        },
    })

    return jsonify(data)


@app.route("/api/motor", methods=["POST", "OPTIONS"])
def api_motor():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    try:
        data = parse_json_body()
        speed = get_number(data, "speed")
        validate_range(speed, -100, 100, "speed")

        applied_speed = car.set_motor_speed(int(speed))

        with state_lock:
            server_state["last_drive_time"] = time.time()

        return jsonify({
            "ok": True,
            "input_speed": int(speed),
            "applied_speed": applied_speed,
        })

    except ValueError as e:
        return make_error(e, 400)
    except Exception as e:
        return make_error(e, 500)


@app.route("/api/steering", methods=["POST", "OPTIONS"])
def api_steering():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    try:
        data = parse_json_body()
        angle = get_number(data, "angle")
        validate_range(angle, config.MIN_STEERING_ANGLE, config.MAX_STEERING_ANGLE, "angle")

        applied_angle = car.set_steering_angle(int(angle))

        return jsonify({
            "ok": True,
            "angle": applied_angle,
        })

    except ValueError as e:
        return make_error(e, 400)
    except Exception as e:
        return make_error(e, 500)


@app.route("/api/drive", methods=["POST", "OPTIONS"])
def api_drive():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    try:
        data = parse_json_body()
        x = get_number(data, "x")
        y = get_number(data, "y")

        validate_range(x, -1.0, 1.0, "x")
        validate_range(y, -1.0, 1.0, "y")

        result = car.drive_by_joystick(x, y)

        with state_lock:
            server_state["last_drive_time"] = time.time()

        return jsonify({
            "ok": True,
            **result,
        })

    except ValueError as e:
        return make_error(e, 400)
    except Exception as e:
        return make_error(e, 500)


@app.route("/api/camera/pan_tilt", methods=["POST", "OPTIONS"])
def api_camera_pan_tilt():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    try:
        data = parse_json_body()
        pan = get_number(data, "pan")
        tilt = get_number(data, "tilt")

        validate_range(pan, config.MIN_PAN, config.MAX_PAN, "pan")
        validate_range(tilt, config.MIN_TILT, config.MAX_TILT, "tilt")

        result = camera_pan_tilt.set_pan_tilt(int(pan), int(tilt))

        return jsonify({
            "ok": True,
            **result,
        })

    except ValueError as e:
        return make_error(e, 400)
    except Exception as e:
        return make_error(e, 500)


@app.route("/api/camera/start", methods=["POST", "OPTIONS"])
def api_camera_start():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    available = camera_stream.start()

    return jsonify({
        "ok": True,
        "enabled": True,
        "camera_available": available,
        "message": camera_stream.get_status()["last_message"],
    })


@app.route("/api/camera/stop", methods=["POST", "OPTIONS"])
def api_camera_stop():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    camera_stream.stop()

    return jsonify({
        "ok": True,
        "enabled": False,
    })


@app.route("/video_feed", methods=["GET"])
def video_feed():
    return Response(
        camera_stream.mjpeg_generator(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/api/sound/tone", methods=["POST", "OPTIONS"])
def api_sound_tone():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    try:
        data = parse_json_body()
        freq = get_number(data, "freq")
        duration = get_number(data, "duration")

        validate_range(freq, 50, 3000, "freq")
        validate_range(duration, 0.05, 5.0, "duration")

        result = sound.play_tone(freq=freq, duration=duration)

        return jsonify({
            "ok": True,
            **result,
        })

    except ValueError as e:
        return make_error(e, 400)
    except Exception as e:
        return make_error(e, 500)


@app.route("/api/sound/tts", methods=["POST", "OPTIONS"])
def api_sound_tts():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    try:
        data = parse_json_body()

        if "text" not in data:
            raise ValueError("'text' 값이 필요합니다.")

        text = str(data["text"]).strip()

        if not text:
            raise ValueError("'text' 값이 비어 있습니다.")

        if len(text) > 120:
            raise ValueError("'text' 길이는 120자 이하로 제한합니다.")

        result = sound.play_tts(text)

        return jsonify({
            "ok": True,
            **result,
        })

    except ValueError as e:
        return make_error(e, 400)
    except Exception as e:
        return make_error(e, 500)


@app.route("/api/stop", methods=["POST", "OPTIONS"])
def api_stop():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    car.stop()

    with state_lock:
        server_state["last_drive_time"] = 0.0

    return jsonify({
        "ok": True,
        "message": "motor stopped and steering centered",
        "car": car.get_status(),
    })


def watchdog_loop():
    """
    조이스틱 또는 모터 명령이 끊겼을 때 차량이 계속 움직이는 것을 막기 위한 안전 정지 루프입니다.
    """
    while True:
        time.sleep(0.1)

        with state_lock:
            last_drive_time = server_state["last_drive_time"]

        if last_drive_time <= 0:
            continue

        elapsed = time.time() - last_drive_time
        car_status = car.get_status()

        if elapsed > config.DRIVE_TIMEOUT_SEC and car_status["speed"] != 0:
            print("[WATCHDOG] command timeout. auto stop.")
            car.stop()

            with state_lock:
                server_state["last_drive_time"] = 0.0


def main():
    global car, camera_stream, camera_pan_tilt, sound

    parser = argparse.ArgumentParser(description="Autocar Flask API server")
    parser.add_argument("--host", default=config.HOST)
    parser.add_argument("--port", type=int, default=config.PORT)
    parser.add_argument("--camera-index", type=int, default=config.CAMERA_INDEX)
    parser.add_argument("--real", action="store_true", help="실제 하드웨어 제어 클래스를 사용합니다.")
    args = parser.parse_args()

    if args.real:
        mode = "real"
        car = RealCarController(
            max_speed=config.MAX_SPEED,
            min_steering=config.MIN_STEERING_ANGLE,
            max_steering=config.MAX_STEERING_ANGLE,
        )
        camera_pan_tilt = RealCameraPanTilt(
            min_pan=config.MIN_PAN,
            max_pan=config.MAX_PAN,
            min_tilt=config.MIN_TILT,
            max_tilt=config.MAX_TILT,
        )
        sound = RealSoundController()
    else:
        mode = "mock"
        car = MockCarController(
            max_speed=config.MAX_SPEED,
            min_steering=config.MIN_STEERING_ANGLE,
            max_steering=config.MAX_STEERING_ANGLE,
        )
        camera_pan_tilt = MockCameraPanTilt(
            min_pan=config.MIN_PAN,
            max_pan=config.MAX_PAN,
            min_tilt=config.MIN_TILT,
            max_tilt=config.MAX_TILT,
        )
        sound = MockSoundController()

    camera_stream = CameraStream(
        camera_index=args.camera_index,
        width=config.CAMERA_WIDTH,
        height=config.CAMERA_HEIGHT,
        fps=config.CAMERA_FPS,
        jpeg_quality=config.JPEG_QUALITY,
    )

    with state_lock:
        server_state["mode"] = mode

    threading.Thread(target=watchdog_loop, daemon=True).start()

    print("=" * 60)
    print("[AUTOCAR API SERVER]")
    print(f"mode       : {mode}")
    print(f"host       : {args.host}")
    print(f"port       : {args.port}")
    print(f"camera     : {args.camera_index}")
    print(f"status URL : http://<AUTOCAR_IP>:{args.port}/api/status")
    print("=" * 60)

    app.run(
        host=args.host,
        port=args.port,
        threaded=True,
        use_reloader=False,
    )


if __name__ == "__main__":
    main()
