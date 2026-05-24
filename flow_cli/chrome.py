"""Chrome management utilities"""

import subprocess
import time
import sys
from pathlib import Path


def get_chrome_path():
    """Get Chrome executable path based on platform"""
    if sys.platform == 'darwin':
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif sys.platform == 'linux':
        paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser"
        ]
        for path in paths:
            if Path(path).exists():
                return path
        return None
    elif sys.platform == 'win32':
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
        for path in paths:
            if Path(path).exists():
                return path
        return None
    return None


def start_chrome(port: int = 9222, profile: str = "/tmp/flow_chrome_debug") -> bool:
    """启动 Chrome with remote debugging"""
    chrome_path = get_chrome_path()

    if not chrome_path:
        print("❌ 未找到 Chrome 可执行文件")
        return False

    # 先停止现有的 Chrome
    stop_chrome()

    print(f"启动 Chrome...")
    print(f"  路径: {chrome_path}")
    print(f"  端口: {port}")
    print(f"  Profile: {profile}")

    # 启动 Chrome
    try:
        subprocess.Popen([
            chrome_path,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile}",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 等待启动
        time.sleep(3)
        return True

    except Exception as e:
        print(f"启动失败: {e}")
        return False


def stop_chrome() -> bool:
    """停止 Chrome"""
    try:
        if sys.platform == 'darwin':
            subprocess.run(['killall', 'Google Chrome'],
                          stderr=subprocess.DEVNULL)
        elif sys.platform == 'linux':
            subprocess.run(['killall', 'chrome'],
                          stderr=subprocess.DEVNULL)
        elif sys.platform == 'win32':
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'],
                          stderr=subprocess.DEVNULL)

        time.sleep(2)
        return True

    except Exception as e:
        print(f"停止失败: {e}")
        return False
