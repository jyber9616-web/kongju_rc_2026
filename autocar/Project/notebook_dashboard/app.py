# app.py
"""
노트북에서 실행하는 pywebview 대시보드 앱입니다.

실행:
    python app.py http://AUTOCAR_IP:8000

예:
    python app.py http://192.168.55.1:8000
"""

import os
import sys
from pathlib import Path

import webview


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_HTML = BASE_DIR / "index.html"


def get_autocar_url():
    if len(sys.argv) >= 2:
        return sys.argv[1].rstrip("/")

    return os.environ.get("AUTOCAR_URL", "http://192.168.55.1:8000").rstrip("/")


def write_config_js(autocar_url):
    """
    JavaScript에서 API 주소를 읽을 수 있도록 실행 시 config.js를 생성합니다.
    """
    STATIC_DIR.mkdir(exist_ok=True)

    config_path = STATIC_DIR / "config.js"
    config_path.write_text(
        f'window.AUTOCAR_URL = "{autocar_url}";\n',
        encoding="utf-8",
    )


def main():
    autocar_url = get_autocar_url()
    write_config_js(autocar_url)

    if not INDEX_HTML.exists():
        raise FileNotFoundError(f"index.html을 찾을 수 없습니다: {INDEX_HTML}")

    print("=" * 60)
    print("[NOTEBOOK DASHBOARD]")
    print(f"Autocar API URL: {autocar_url}")
    print("=" * 60)

    webview.create_window(
        title="Autocar Dashboard",
        url=INDEX_HTML.as_uri(),
        width=1180,
        height=820,
        resizable=True,
    )

    webview.start(debug=True)


if __name__ == "__main__":
    main()
