# sound_controller.py
"""
소리/TTS 제어 클래스입니다.

과제 조건:
- /api/sound/tone: 지정한 주파수와 시간으로 소리 재생
- /api/sound/tts: 인터넷 가능 시 gTTS, 인터넷 불가 시 espeak 또는 piper 사용 가능하도록 설계
- Mock에서는 print로 sound 명령을 확인할 수 있어야 함
"""

import math
import os
import subprocess
import tempfile
import wave


class MockSoundController:
    """
    Mock 소리 제어 클래스입니다.
    print로 명령을 확인하고, 실행 환경에 aplay/espeak/gTTS가 있으면 실제 재생도 시도합니다.
    """

    def __init__(self):
        self.last_sound = "none"
        print("[SOUND] MockSoundController ready")

    def make_tone_wav(self, freq, duration, wav_path, sample_rate=44100):
        freq = float(freq)
        duration = float(duration)

        with wave.open(wav_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)

            total_samples = int(sample_rate * duration)

            for i in range(total_samples):
                t = i / sample_rate
                sample = int(18000 * math.sin(2 * math.pi * freq * t))
                wf.writeframesraw(sample.to_bytes(2, byteorder="little", signed=True))

    def play_wav(self, wav_path):
        """
        Linux에서는 aplay를 우선 사용합니다.
        없으면 print-only로 처리합니다.
        """
        try:
            subprocess.Popen(["aplay", wav_path])
            return {
                "played": True,
                "player": "aplay",
            }
        except FileNotFoundError:
            print("[SOUND] aplay not found. print-only mode.")
            return {
                "played": False,
                "player": "print-only",
            }
        except Exception as e:
            print(f"[SOUND ERROR] {e}")
            return {
                "played": False,
                "player": "aplay",
                "error": str(e),
            }

    def play_tone(self, freq=440, duration=0.5):
        freq = float(freq)
        duration = float(duration)

        self.last_sound = f"tone freq={freq}, duration={duration}"
        print(f"[TONE MOCK] freq={freq}, duration={duration}")

        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                wav_path = tmp.name

            self.make_tone_wav(freq, duration, wav_path)
            play_result = self.play_wav(wav_path)

            return {
                "freq": freq,
                "duration": duration,
                **play_result,
            }

        except Exception as e:
            print(f"[TONE ERROR] {e}")
            return {
                "freq": freq,
                "duration": duration,
                "played": False,
                "error": str(e),
            }

    def play_tts_with_gtts(self, text):
        """
        인터넷이 가능하고 gTTS가 설치되어 있을 때 사용하는 방식입니다.
        gTTS가 없거나 실패하면 None을 반환하고 다른 방식으로 fallback합니다.
        """
        try:
            from gtts import gTTS
        except ImportError:
            return None

        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                mp3_path = tmp.name

            tts = gTTS(text=text, lang="en")
            tts.save(mp3_path)

            # mpg123가 있으면 재생합니다.
            try:
                subprocess.Popen(["mpg123", mp3_path])
                return {
                    "played": True,
                    "engine": "gTTS+mpg123",
                }
            except FileNotFoundError:
                print(f"[TTS] gTTS mp3 saved: {mp3_path}, but mpg123 not found.")
                return {
                    "played": False,
                    "engine": "gTTS",
                    "file": mp3_path,
                    "message": "mpg123 not found",
                }

        except Exception as e:
            print(f"[GTTS ERROR] {e}")
            return None

    def play_tts_with_local_engine(self, text):
        """
        인터넷이 안 되는 경우를 대비한 로컬 TTS fallback입니다.
        """
        commands = [
            ["espeak-ng", text],
            ["espeak", text],
            ["spd-say", text],
            ["piper", "--help"],
        ]

        for cmd in commands:
            try:
                if cmd[0] == "piper":
                    # piper는 모델 파일이 필요하므로 실제 실행 대신 설치 여부만 확인합니다.
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print("[TTS] piper installed, but model path is not configured.")
                    continue

                subprocess.Popen(cmd)
                return {
                    "played": True,
                    "engine": cmd[0],
                }

            except FileNotFoundError:
                continue
            except Exception as e:
                return {
                    "played": False,
                    "engine": cmd[0],
                    "error": str(e),
                }

        return {
            "played": False,
            "engine": "print-only",
            "message": "no TTS engine found",
        }

    def play_tts(self, text):
        text = str(text).strip()

        self.last_sound = f"tts text={text}"
        print(f"[TTS MOCK] {text}")

        # 1순위: gTTS
        gtts_result = self.play_tts_with_gtts(text)
        if gtts_result is not None:
            return {
                "text": text,
                **gtts_result,
            }

        # 2순위: espeak/espeak-ng/spd-say/piper
        local_result = self.play_tts_with_local_engine(text)

        return {
            "text": text,
            **local_result,
        }

    def get_status(self):
        return {
            "last_sound": self.last_sound,
        }


class RealSoundController(MockSoundController):
    """
    실제 스피커/TTS 장치가 따로 있으면 이 클래스에서 교체합니다.
    현재는 MockSoundController와 같은 방식으로 동작합니다.
    """

    def __init__(self):
        super().__init__()
        print("[SOUND] RealSoundController selected")
