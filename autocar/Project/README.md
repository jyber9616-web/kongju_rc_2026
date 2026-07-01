# Autocar Mini Assignment

## 1. 전체 프로젝트 구조

```text
autocar_api/
├── server.py
├── car_controller.py
├── camera_controller.py
├── sound_controller.py
└── config.py

notebook_dashboard/
├── app.py
├── index.html
└── static/
    ├── style.css
    └── main.js

README.md
```

## 2. 각 파일의 역할

### autocar_api/server.py

Autocar 내부에서 실행하는 Flask API 서버입니다.

주요 기능:

- `/api/status`
- `/api/motor`
- `/api/steering`
- `/api/drive`
- `/api/camera/pan_tilt`
- `/api/camera/start`
- `/api/camera/stop`
- `/video_feed`
- `/api/sound/tone`
- `/api/sound/tts`
- `/api/stop`

### autocar_api/car_controller.py

모터와 조향 서보 제어 담당 파일입니다.

- `MockCarController`: 실제 차량을 움직이지 않고 print로 명령 확인
- `RealCarController`: 실제 Autocar 라이브러리 또는 GPIO 코드로 교체할 위치

### autocar_api/camera_controller.py

카메라 pan/tilt와 OpenCV MJPEG 스트리밍 담당 파일입니다.

- `MockCameraPanTilt`: pan/tilt 명령을 print로 확인
- `RealCameraPanTilt`: 실제 pan/tilt 서보 코드 작성 위치
- `CameraStream`: `/video_feed` MJPEG 스트리밍

### autocar_api/sound_controller.py

소리와 TTS 담당 파일입니다.

- `/api/sound/tone`: 지정 주파수 tone 재생
- `/api/sound/tts`: gTTS, espeak, espeak-ng, spd-say fallback 구조

### autocar_api/config.py

포트, 속도 제한, 조향 제한, pan/tilt 제한, 카메라 설정 파일입니다.

### notebook_dashboard/app.py

노트북에서 실행하는 pywebview 앱입니다.  
실행할 때 Autocar API 서버 주소를 인자로 받습니다.

### notebook_dashboard/index.html

대시보드 화면입니다.

구성:

- 카메라 화면 영역
- 조이스틱 영역
- 전진/후진/좌/우/정지 버튼
- 속도 슬라이더
- 카메라 pan/tilt 슬라이더
- 소리 재생 버튼
- TTS 입력창
- 현재 상태 표시 영역

### notebook_dashboard/static/main.js

fetch API로 Autocar API 서버에 명령을 전송합니다.

### notebook_dashboard/static/style.css

대시보드 화면 스타일입니다.

## 3. Autocar API 서버 실행 방법

### 패키지 설치

```bash
sudo apt update
sudo apt install -y python3-flask python3-opencv espeak-ng alsa-utils
```

gTTS까지 사용할 경우:

```bash
pip install gTTS
```

### 파일 전송

노트북에서:

```bash
scp -r autocar_api ubuntu@AUTOCAR_IP:/home/ubuntu/
```

예:

```bash
scp -r autocar_api ubuntu@192.168.55.1:/home/ubuntu/
```

### Mock 모드 실행

Autocar에서:

```bash
cd /home/ubuntu/autocar_api
python3 server.py
```

Mock 모드에서는 실제 모터/서보가 움직이지 않고 터미널에 명령만 출력됩니다.

### 실제 하드웨어 모드 실행

`RealCarController`, `RealCameraPanTilt` 안의 TODO 코드를 실제 하드웨어 코드로 교체한 뒤 실행합니다.

```bash
cd /home/ubuntu/autocar_api
python3 server.py --real
```

## 4. 노트북 pywebview 대시보드 실행 방법

### 패키지 설치

```bash
pip install pywebview
```

### 실행

```bash
cd notebook_dashboard
python app.py http://AUTOCAR_IP:8000
```

예:

```bash
python app.py http://192.168.55.1:8000
```

## 5. API 목록과 테스트 방법

### 상태 확인

```bash
curl http://AUTOCAR_IP:8000/api/status
```

### 모터 제어

```bash
curl -X POST http://AUTOCAR_IP:8000/api/motor \
  -H "Content-Type: application/json" \
  -d '{"speed":30}'
```

입력 범위:

```text
speed: -100 ~ 100
양수: 전진
음수: 후진
0: 정지
```

### 조향 제어

```bash
curl -X POST http://AUTOCAR_IP:8000/api/steering \
  -H "Content-Type: application/json" \
  -d '{"angle":10}'
```

입력 범위:

```text
angle: -45 ~ 45
음수: 좌회전
양수: 우회전
```

### 조이스틱 제어

```bash
curl -X POST http://AUTOCAR_IP:8000/api/drive \
  -H "Content-Type: application/json" \
  -d '{"x":0.3,"y":0.8}'
```

입력 범위:

```text
x: -1.0 ~ 1.0
y: -1.0 ~ 1.0
x는 조향, y는 속도로 변환
```

### 카메라 pan/tilt

```bash
curl -X POST http://AUTOCAR_IP:8000/api/camera/pan_tilt \
  -H "Content-Type: application/json" \
  -d '{"pan":30,"tilt":10}'
```

입력 범위:

```text
pan: -90 ~ 90
tilt: -60 ~ 60
```

### 카메라 켜기

```bash
curl -X POST http://AUTOCAR_IP:8000/api/camera/start
```

### 카메라 끄기

```bash
curl -X POST http://AUTOCAR_IP:8000/api/camera/stop
```

### 카메라 스트리밍

브라우저에서:

```text
http://AUTOCAR_IP:8000/video_feed
```

### tone 재생

```bash
curl -X POST http://AUTOCAR_IP:8000/api/sound/tone \
  -H "Content-Type: application/json" \
  -d '{"freq":440,"duration":0.5}'
```

### TTS

```bash
curl -X POST http://AUTOCAR_IP:8000/api/sound/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"hello autocar"}'
```

### 긴급 정지

```bash
curl -X POST http://AUTOCAR_IP:8000/api/stop
```

## 6. 테스트 순서

1. Autocar에 `autocar_api` 폴더를 scp로 전송
2. Autocar에서 `python3 server.py` 실행
3. 노트북에서 `curl http://AUTOCAR_IP:8000/api/status` 확인
4. `/api/motor`, `/api/steering`, `/api/drive`를 curl로 테스트
5. Autocar 터미널에 Mock print가 출력되는지 확인
6. 노트북에서 `python app.py http://AUTOCAR_IP:8000` 실행
7. pywebview 대시보드에서 버튼, 조이스틱, 슬라이더, TTS, 카메라 버튼 테스트
8. 카메라가 없을 경우 `camera not available` 더미 화면 또는 fallback 이미지가 나오는지 확인
9. 실제 하드웨어 코드 작성 후 `python3 server.py --real` 실행

## 7. 실제 하드웨어 코드로 교체해야 하는 위치

### 모터/조향

파일:

```text
autocar_api/car_controller.py
```

수정 위치:

```python
class RealCarController(MockCarController):
    def __init__(...):
        # 실제 모터/서보 초기화

    def set_motor_speed(...):
        # 실제 모터 PWM 제어

    def set_steering_angle(...):
        # 실제 조향 서보 제어
```

### 카메라 pan/tilt

파일:

```text
autocar_api/camera_controller.py
```

수정 위치:

```python
class RealCameraPanTilt(MockCameraPanTilt):
    def __init__(...):
        # 실제 pan/tilt 서보 초기화

    def set_pan_tilt(...):
        # 실제 pan/tilt 서보 제어
```

## 8. 안전 조건

- `/api/motor`는 -100 ~ 100만 허용합니다.
- 실제 적용 속도는 `config.py`의 `MAX_SPEED`로 제한합니다.
- `/api/steering`은 -45 ~ 45만 허용합니다.
- `/api/drive`는 x, y 모두 -1.0 ~ 1.0만 허용합니다.
- `/api/stop`은 모터를 0으로 만들고 조향을 중앙으로 복귀시킵니다.
- 조이스틱 명령이 끊기면 watchdog이 자동으로 정지합니다.
- 잘못된 입력은 `{ "ok": false, "error": "..." }` JSON으로 반환합니다.
