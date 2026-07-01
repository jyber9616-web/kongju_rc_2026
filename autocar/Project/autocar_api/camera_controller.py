# camera_controller.py
"""
카메라 스트리밍과 pan/tilt 서보 제어 클래스입니다.

과제 조건:
- /video_feed에서 OpenCV 카메라 영상을 MJPEG로 제공
- pywebview의 img 태그에서 볼 수 있어야 함
- 카메라가 없는 환경에서도 테스트할 수 있도록 더미 이미지 또는 camera not available 처리
- pan/tilt는 Mock print로 먼저 확인
"""

import base64
import threading
import time

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


# OpenCV/Pillow가 없는 환경에서도 /video_feed가 완전히 죽지 않도록 사용하는 1x1 JPEG입니다.
FALLBACK_JPEG = base64.b64decode(
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////"
    "2wBDAf//////////////////////////////////////////////////////////////////////////////////////"
    "wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAX/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIQAxAAAAF//8QAFBAB"
    "AAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABBQJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAwEBPwF//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/a"
    "AAgBAgEBPwF//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQAGPwJ//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPyF//9k="
)


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


class MockCameraPanTilt:
    """
    카메라 pan/tilt 서보 Mock 클래스입니다.
    """

    def __init__(self, min_pan=-90, max_pan=90, min_tilt=-60, max_tilt=60):
        self.min_pan = int(min_pan)
        self.max_pan = int(max_pan)
        self.min_tilt = int(min_tilt)
        self.max_tilt = int(max_tilt)
        self.pan = 0
        self.tilt = 0
        self.last_command = "none"
        print("[CAMERA] MockCameraPanTilt ready")

    def set_pan_tilt(self, pan, tilt):
        input_pan = int(pan)
        input_tilt = int(tilt)

        applied_pan = int(clamp(input_pan, self.min_pan, self.max_pan))
        applied_tilt = int(clamp(input_tilt, self.min_tilt, self.max_tilt))

        self.pan = applied_pan
        self.tilt = applied_tilt
        self.last_command = f"pan={applied_pan}, tilt={applied_tilt}"

        print(
            f"[PAN/TILT MOCK] input_pan={input_pan}, input_tilt={input_tilt}, "
            f"applied_pan={applied_pan}, applied_tilt={applied_tilt}"
        )

        return {
            "pan": applied_pan,
            "tilt": applied_tilt,
        }

    def get_status(self):
        return {
            "pan": self.pan,
            "tilt": self.tilt,
            "last_command": self.last_command,
        }


class RealCameraPanTilt(MockCameraPanTilt):
    """
    실제 pan/tilt 서보 코드로 교체할 클래스입니다.
    """

    def __init__(self, min_pan=-90, max_pan=90, min_tilt=-60, max_tilt=60):
        super().__init__(
            min_pan=min_pan,
            max_pan=max_pan,
            min_tilt=min_tilt,
            max_tilt=max_tilt,
        )
        print("[CAMERA] RealCameraPanTilt selected")

        # TODO:
        # 실제 pan/tilt 서보 초기화 코드를 여기에 작성하십시오.
        #
        # 예시:
        # from gpiozero import Servo
        # self.pan_servo = Servo(13)
        # self.tilt_servo = Servo(19)

    def set_pan_tilt(self, pan, tilt):
        result = super().set_pan_tilt(pan, tilt)

        # TODO:
        # 실제 pan/tilt 서보 제어 코드 작성 위치
        #
        # pan_value = result["pan"] / 90.0
        # tilt_value = result["tilt"] / 60.0
        # self.pan_servo.value = pan_value
        # self.tilt_servo.value = tilt_value

        print(f"[PAN/TILT REAL TODO] pan={result['pan']}, tilt={result['tilt']}")
        return result


class CameraStream:
    """
    OpenCV VideoCapture를 MJPEG 스트리밍으로 바꾸는 클래스입니다.
    """

    def __init__(self, camera_index=0, width=640, height=480, fps=20, jpeg_quality=75):
        self.camera_index = int(camera_index)
        self.width = int(width)
        self.height = int(height)
        self.fps = int(fps)
        self.jpeg_quality = int(jpeg_quality)
        self.cap = None
        self.enabled = False
        self.last_message = "camera stopped"
        self.lock = threading.Lock()

    def start(self):
        self.enabled = True

        if cv2 is None:
            self.last_message = "OpenCV not installed. fallback image mode."
            print(f"[VIDEO] {self.last_message}")
            return False

        with self.lock:
            if self.cap is None:
                self.cap = cv2.VideoCapture(self.camera_index)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                self.cap.set(cv2.CAP_PROP_FPS, self.fps)

            if not self.cap.isOpened():
                self.last_message = "camera not available. dummy image mode."
                print(f"[VIDEO] {self.last_message}")
                return False

        self.last_message = "camera started"
        print("[VIDEO] camera started")
        return True

    def stop(self):
        self.enabled = False

        with self.lock:
            if self.cap is not None:
                self.cap.release()
                self.cap = None

        self.last_message = "camera stopped"
        print("[VIDEO] camera stopped")

    def camera_available(self):
        if cv2 is None:
            return False

        with self.lock:
            return self.cap is not None and self.cap.isOpened()

    def get_status(self):
        return {
            "enabled": self.enabled,
            "opencv_available": cv2 is not None,
            "camera_available": self.camera_available(),
            "camera_index": self.camera_index,
            "last_message": self.last_message,
        }

    def make_dummy_frame(self, text):
        """
        OpenCV가 있으면 글자가 적힌 더미 JPEG를 만들고,
        OpenCV 자체가 없으면 1x1 fallback JPEG를 반환합니다.
        """
        if cv2 is None or np is None:
            return FALLBACK_JPEG

        frame = np.zeros((360, 640, 3), dtype=np.uint8)
        cv2.putText(
            frame,
            text,
            (45, 180),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        ok, buffer = cv2.imencode(".jpg", frame)

        if not ok:
            return FALLBACK_JPEG

        return buffer.tobytes()

    def read_jpeg(self):
        if not self.enabled:
            return self.make_dummy_frame("camera off")

        if cv2 is None:
            return self.make_dummy_frame("OpenCV not installed")

        with self.lock:
            if self.cap is None or not self.cap.isOpened():
                return self.make_dummy_frame("camera not available")

            ok, frame = self.cap.read()

        if not ok or frame is None:
            return self.make_dummy_frame("no camera frame")

        ok, buffer = cv2.imencode(
            ".jpg",
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality],
        )

        if not ok:
            return self.make_dummy_frame("jpeg encode error")

        return buffer.tobytes()

    def mjpeg_generator(self):
        """
        Flask Response에서 사용하는 MJPEG 제너레이터입니다.
        """
        delay = 1.0 / max(self.fps, 1)

        while True:
            jpg = self.read_jpeg()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"
            )

            time.sleep(delay)
