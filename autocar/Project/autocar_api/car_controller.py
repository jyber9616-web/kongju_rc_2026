# car_controller.py
"""
모터와 조향 서보 제어 클래스입니다.

과제 조건:
- 먼저 Mock 클래스로 동작해야 함
- Mock에서는 print 문으로 motor, steering 명령을 확인할 수 있어야 함
- 나중에 실제 Autocar 라이브러리/GPIO/서보 제어 코드로 교체 가능해야 함
"""

from dataclasses import dataclass


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


@dataclass
class CarStatus:
    speed: int = 0
    steering_angle: int = 0
    last_command: str = "none"


class MockCarController:
    """
    실제 차량을 움직이지 않고 명령만 출력하는 Mock 클래스입니다.
    """

    def __init__(self, max_speed=60, min_steering=-45, max_steering=45):
        self.max_speed = int(max_speed)
        self.min_steering = int(min_steering)
        self.max_steering = int(max_steering)
        self.status = CarStatus()
        print("[CAR] MockCarController ready")

    def set_motor_speed(self, speed):
        """
        /api/motor에서 호출됩니다.

        speed:
            -100 ~ 100 입력
            양수: 전진
            음수: 후진
            0: 정지
        """
        input_speed = int(speed)
        applied_speed = int(clamp(input_speed, -self.max_speed, self.max_speed))

        self.status.speed = applied_speed
        self.status.last_command = f"motor speed={applied_speed}"

        if applied_speed > 0:
            direction = "forward"
        elif applied_speed < 0:
            direction = "backward"
        else:
            direction = "stop"

        print(
            f"[MOTOR MOCK] input_speed={input_speed}, "
            f"applied_speed={applied_speed}, direction={direction}"
        )

        return applied_speed

    def set_steering_angle(self, angle):
        """
        /api/steering에서 호출됩니다.

        angle:
            -45 ~ 45
            음수: 좌회전
            양수: 우회전
            0: 중앙
        """
        input_angle = int(angle)
        applied_angle = int(clamp(input_angle, self.min_steering, self.max_steering))

        self.status.steering_angle = applied_angle
        self.status.last_command = f"steering angle={applied_angle}"

        if applied_angle < 0:
            direction = "left"
        elif applied_angle > 0:
            direction = "right"
        else:
            direction = "center"

        print(
            f"[STEERING MOCK] input_angle={input_angle}, "
            f"applied_angle={applied_angle}, direction={direction}"
        )

        return applied_angle

    def drive_by_joystick(self, x, y):
        """
        /api/drive에서 호출됩니다.

        x:
            -1.0 ~ 1.0 조이스틱 좌우값
            x < 0: 좌회전
            x > 0: 우회전

        y:
            -1.0 ~ 1.0 조이스틱 전후값
            y > 0: 전진
            y < 0: 후진
        """
        x = float(clamp(float(x), -1.0, 1.0))
        y = float(clamp(float(y), -1.0, 1.0))

        speed = int(y * self.max_speed)
        steering_angle = int(x * self.max_steering)

        applied_speed = self.set_motor_speed(speed)
        applied_angle = self.set_steering_angle(steering_angle)

        self.status.last_command = (
            f"drive x={x:.2f}, y={y:.2f}, "
            f"speed={applied_speed}, steering={applied_angle}"
        )

        print(
            f"[DRIVE MOCK] x={x:.2f}, y={y:.2f}, "
            f"speed={applied_speed}, steering={applied_angle}"
        )

        return {
            "x": x,
            "y": y,
            "speed": applied_speed,
            "steering_angle": applied_angle,
        }

    def stop(self):
        """
        /api/stop에서 호출됩니다.
        모터 속도를 0으로 만들고 조향을 중앙으로 복귀합니다.
        """
        self.set_motor_speed(0)
        self.set_steering_angle(0)
        self.status.last_command = "stop"
        print("[STOP MOCK] motor=0, steering=0")

    def get_status(self):
        return {
            "speed": self.status.speed,
            "steering_angle": self.status.steering_angle,
            "last_command": self.status.last_command,
        }


class RealCarController(MockCarController):
    """
    실제 하드웨어 코드로 교체할 클래스입니다.

    현재는 안전을 위해 실제 제어 코드를 직접 넣지 않고 TODO 위치를 표시했습니다.
    --real 옵션으로 실행하면 이 클래스가 선택됩니다.
    """

    def __init__(self, max_speed=60, min_steering=-45, max_steering=45):
        super().__init__(
            max_speed=max_speed,
            min_steering=min_steering,
            max_steering=max_steering,
        )
        print("[CAR] RealCarController selected")

        # TODO:
        # 실제 Autocar 라이브러리 또는 GPIO/PWM 초기화 코드를 여기에 작성하십시오.
        #
        # 예시:
        # from gpiozero import Motor, Servo
        # self.motor = Motor(forward=17, backward=18)
        # self.steering_servo = Servo(12)
        #
        # 실제 핀 번호는 본인 차량 배선에 맞게 수정해야 합니다.

    def set_motor_speed(self, speed):
        applied_speed = super().set_motor_speed(speed)

        # TODO:
        # 실제 모터 제어 코드 작성 위치
        #
        # pwm_value = abs(applied_speed) / 100.0
        #
        # if applied_speed > 0:
        #     self.motor.forward(pwm_value)
        # elif applied_speed < 0:
        #     self.motor.backward(pwm_value)
        # else:
        #     self.motor.stop()

        print(f"[MOTOR REAL TODO] applied_speed={applied_speed}")
        return applied_speed

    def set_steering_angle(self, angle):
        applied_angle = super().set_steering_angle(angle)

        # TODO:
        # 실제 조향 서보 제어 코드 작성 위치
        #
        # servo_value = applied_angle / self.max_steering
        # self.steering_servo.value = servo_value

        print(f"[STEERING REAL TODO] applied_angle={applied_angle}")
        return applied_angle
