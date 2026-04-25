import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

APP_NAME = "CalendarDesktop"
ICON_PATH = "assets/icon.ico"
ENTRY_POINT = "desktop/main.py"
BUILD_DIR = "dist"

def run_pyinstaller():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_NAME,
        "--windowed",
        "--icon", ICON_PATH if os.path.exists(ICON_PATH) else None,
        "--add-data", f"{os.path.join('desktop', 'ui')}{';' if platform.system() == 'Windows' else ':'}ui",
        "--add-data", f"{os.path.join('desktop', 'core')}{';' if platform.system() == 'Windows' else ':'}core",
        "--hidden-import", "customtkinter",
        "--hidden-import", "httpx",
        "--hidden-import", "apscheduler",
        "--hidden-import", "dateutil",
        "--clean",
        "--noconfirm",
        ENTRY_POINT
    ]
    cmd = [c for c in cmd if c is not None]
    subprocess.run(cmd, check=True)

def setup_autostart():
    if platform.system() == "Windows":
        import winreg
        try:
            exe_path = os.path.abspath(os.path.join(BUILD_DIR, APP_NAME, f"{APP_NAME}.exe"))
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
        except Exception:
            pass
    else:
        desktop_file = os.path.expanduser("~/.config/autostart/calendar.desktop")
        os.makedirs(os.path.dirname(desktop_file), exist_ok=True)
        exe_path = os.path.abspath(os.path.join(BUILD_DIR, APP_NAME))
        with open(desktop_file, "w") as f:
            f.write(f"[Desktop Entry]\nType=Application\nExec={exe_path}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName={APP_NAME}\n")

def cleanup():
    for d in ["build", "__pycache__", f"{APP_NAME}.spec"]:
        p = Path(d)
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

if __name__ == "__main__":
    run_pyinstaller()
    setup_autostart()
    cleanup()
    print("Сборка завершена.")