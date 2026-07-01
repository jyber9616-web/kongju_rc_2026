# config.py
"""
Autocar API 서버 설정 파일입니다.
과제 조건에 맞게 서버 포트, 속도 제한, 조향 제한, 카메라 설정을 분리했습니다.
"""

HOST = "0.0.0.0"
PORT = 8000

# /api/motor 입력은 -100 ~ 100을 받지만,
# 실제 적용 속도는 안전을 위해 MAX_SPEED로 제한합니다.
MAX_SPEED = 60

# /api/steering 입력 범위
MIN_STEERING_ANGLE = -45
MAX_STEERING_ANGLE = 45

# /api/camera/pan_tilt 입력 범위
MIN_PAN = -90
MAX_PAN = 90
MIN_TILT = -60
MAX_TILT = 60

# 조이스틱 명령이 끊겼을 때 자동 정지까지 걸리는 시간
DRIVE_TIMEOUT_SEC = 0.8

# OpenCV 카메라 설정
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 20
JPEG_QUALITY = 75
