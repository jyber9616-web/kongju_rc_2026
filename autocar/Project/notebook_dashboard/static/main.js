// main.js

const API_BASE = window.AUTOCAR_URL || "http://192.168.55.1:8000";

const connectionStatus = document.getElementById("connectionStatus");
const statusBox = document.getElementById("statusBox");
const logBox = document.getElementById("logBox");

const joystick = document.getElementById("joystick");
const joystickKnob = document.getElementById("joystickKnob");
const joystickValue = document.getElementById("joystickValue");

const buttonSpeed = document.getElementById("buttonSpeed");
const buttonSpeedValue = document.getElementById("buttonSpeedValue");

const panSlider = document.getElementById("panSlider");
const tiltSlider = document.getElementById("tiltSlider");
const panValue = document.getElementById("panValue");
const tiltValue = document.getElementById("tiltValue");

const cameraImage = document.getElementById("cameraImage");
const cameraPlaceholder = document.getElementById("cameraPlaceholder");

let joystickActive = false;
let joyX = 0.0;
let joyY = 0.0;

function log(message) {
    const time = new Date().toLocaleTimeString();
    logBox.textContent = `[${time}] ${message}\n` + logBox.textContent;
}

function setConnection(ok, message) {
    connectionStatus.textContent = message;

    if (ok) {
        connectionStatus.classList.add("connected");
        connectionStatus.classList.remove("disconnected");
    } else {
        connectionStatus.classList.add("disconnected");
        connectionStatus.classList.remove("connected");
    }
}

async function apiGet(path) {
    const response = await fetch(API_BASE + path);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "GET request failed");
    }

    return data;
}

async function apiPost(path, body = {}) {
    const response = await fetch(API_BASE + path, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || "POST request failed");
    }

    return data;
}

function updateJoystickKnob(x, y) {
    const radius = joystick.clientWidth / 2;
    const knobRadius = joystickKnob.clientWidth / 2;
    const maxMove = radius - knobRadius - 8;

    const left = radius - knobRadius + x * maxMove;
    const top = radius - knobRadius - y * maxMove;

    joystickKnob.style.left = `${left}px`;
    joystickKnob.style.top = `${top}px`;

    joystickValue.textContent = `x=${x.toFixed(2)}, y=${y.toFixed(2)}`;
}

function handleJoystickPointer(event) {
    const rect = joystick.getBoundingClientRect();

    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    let dx = event.clientX - centerX;
    let dy = event.clientY - centerY;

    const maxMove = rect.width / 2 - joystickKnob.clientWidth / 2 - 8;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance > maxMove) {
        dx = dx / distance * maxMove;
        dy = dy / distance * maxMove;
    }

    joyX = dx / maxMove;
    joyY = -dy / maxMove;

    updateJoystickKnob(joyX, joyY);
}

async function sendDrive(x, y) {
    try {
        await apiPost("/api/drive", {x, y});
    } catch (error) {
        setConnection(false, "주행 명령 실패");
        log("drive error: " + error.message);
    }
}

function releaseJoystick() {
    joystickActive = false;
    joyX = 0.0;
    joyY = 0.0;
    updateJoystickKnob(0, 0);
    sendDrive(0, 0);
}

joystick.addEventListener("pointerdown", (event) => {
    joystickActive = true;
    joystick.setPointerCapture(event.pointerId);
    handleJoystickPointer(event);
});

joystick.addEventListener("pointermove", (event) => {
    if (!joystickActive) {
        return;
    }

    handleJoystickPointer(event);
});

joystick.addEventListener("pointerup", releaseJoystick);
joystick.addEventListener("pointercancel", releaseJoystick);

joystick.addEventListener("pointerleave", () => {
    if (joystickActive) {
        releaseJoystick();
    }
});

// 조이스틱 값은 -1.0 ~ 1.0 사이로 정규화하고 일정 주기로 전송합니다.
setInterval(() => {
    if (joystickActive) {
        sendDrive(joyX, joyY);
    }
}, 80);

document.getElementById("stopButton").addEventListener("click", async () => {
    try {
        await apiPost("/api/stop", {});
        updateJoystickKnob(0, 0);
        log("emergency stop");
    } catch (error) {
        log("stop error: " + error.message);
    }
});

document.getElementById("neutralButton").addEventListener("click", async () => {
    try {
        await apiPost("/api/motor", {speed: 0});
        await apiPost("/api/steering", {angle: 0});
        updateJoystickKnob(0, 0);
        log("neutral");
    } catch (error) {
        log("neutral error: " + error.message);
    }
});

buttonSpeed.addEventListener("input", () => {
    buttonSpeedValue.textContent = buttonSpeed.value;
});

document.querySelectorAll("[data-drive]").forEach((button) => {
    button.addEventListener("click", async () => {
        const mode = button.dataset.drive;
        const speed = parseInt(buttonSpeed.value);

        try {
            if (mode === "forward") {
                await apiPost("/api/motor", {speed});
                await apiPost("/api/steering", {angle: 0});
            } else if (mode === "backward") {
                await apiPost("/api/motor", {speed: -speed});
                await apiPost("/api/steering", {angle: 0});
            } else if (mode === "left") {
                await apiPost("/api/steering", {angle: -30});
            } else if (mode === "right") {
                await apiPost("/api/steering", {angle: 30});
            } else if (mode === "stop") {
                await apiPost("/api/stop", {});
            }

            log("button drive: " + mode);
        } catch (error) {
            log("button drive error: " + error.message);
        }
    });
});

async function sendPanTilt() {
    const pan = parseInt(panSlider.value);
    const tilt = parseInt(tiltSlider.value);

    panValue.textContent = pan;
    tiltValue.textContent = tilt;

    try {
        await apiPost("/api/camera/pan_tilt", {pan, tilt});
    } catch (error) {
        log("pan_tilt error: " + error.message);
    }
}

panSlider.addEventListener("input", sendPanTilt);
tiltSlider.addEventListener("input", sendPanTilt);

document.getElementById("cameraCenterButton").addEventListener("click", () => {
    panSlider.value = 0;
    tiltSlider.value = 0;
    sendPanTilt();
});

document.getElementById("cameraOnButton").addEventListener("click", async () => {
    try {
        await apiPost("/api/camera/start", {});
        cameraImage.src = API_BASE + "/video_feed?t=" + Date.now();
        cameraImage.style.display = "block";
        cameraPlaceholder.style.display = "none";
        log("camera on");
    } catch (error) {
        log("camera on error: " + error.message);
    }
});

document.getElementById("cameraOffButton").addEventListener("click", async () => {
    try {
        await apiPost("/api/camera/stop", {});
        cameraImage.src = "";
        cameraImage.style.display = "none";
        cameraPlaceholder.style.display = "block";
        cameraPlaceholder.textContent = "카메라 화면 대기 중";
        log("camera off");
    } catch (error) {
        log("camera off error: " + error.message);
    }
});

document.getElementById("toneButton").addEventListener("click", async () => {
    try {
        await apiPost("/api/sound/tone", {
            freq: 440,
            duration: 0.5,
        });

        log("tone 440Hz");
    } catch (error) {
        log("tone error: " + error.message);
    }
});

document.getElementById("warningToneButton").addEventListener("click", async () => {
    try {
        await apiPost("/api/sound/tone", {
            freq: 880,
            duration: 0.2,
        });

        setTimeout(() => {
            apiPost("/api/sound/tone", {
                freq: 880,
                duration: 0.2,
            });
        }, 300);

        log("warning tone");
    } catch (error) {
        log("warning tone error: " + error.message);
    }
});

document.getElementById("ttsButton").addEventListener("click", async () => {
    const text = document.getElementById("ttsInput").value;

    try {
        await apiPost("/api/sound/tts", {text});
        log("tts: " + text);
    } catch (error) {
        log("tts error: " + error.message);
    }
});

async function refreshStatus() {
    try {
        const data = await apiGet("/api/status");
        statusBox.textContent = JSON.stringify(data, null, 2);
        setConnection(true, "연결됨");
    } catch (error) {
        statusBox.textContent = error.message;
        setConnection(false, "연결 안 됨");
    }
}

setInterval(refreshStatus, 1000);

updateJoystickKnob(0, 0);
buttonSpeedValue.textContent = buttonSpeed.value;
sendPanTilt();
refreshStatus();

log("API_BASE = " + API_BASE);
