# build.py
import os
import subprocess
import sys


def install_pyinstaller():
    """安装 PyInstaller"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller 安装成功!")
    except subprocess.CalledProcessError:
        print("PyInstaller 安装失败!")
        sys.exit(1)


def build_exe():
    """打包成 exe"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=MyApp",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=keyboard",
        "--hidden-import=pydirectinput",
        "--hidden-import=win32gui",
        "--hidden-import=win32con",
        "main_ui.py"
    ]

    try:
        subprocess.check_call(cmd)
        print("打包成功! exe 文件在 dist 文件夹中")
    except subprocess.CalledProcessError:
        print("打包失败!")
        sys.exit(1)


if __name__ == "__main__":
    # 检查是否安装了 PyInstaller
    try:
        import pyinstaller
    except ImportError:
        print("未安装 PyInstaller，正在安装...")
        install_pyinstaller()

    print("开始打包...")
    build_exe()