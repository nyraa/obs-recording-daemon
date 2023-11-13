from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyperclip
import time
import win32gui
import win32con


def launch_cmd(cmd):
    send_keys('{LWIN down}r{LWIN up}')
    run = Application().connect(title='執行', timeout=5)
    pyperclip.copy(cmd)
    run.執行.type_keys('^v{ENTER}')

def call_from_search(keyword):
    send_keys('{LWIN}')
    time.sleep(0.3)

    pyperclip.copy(keyword)
    time.sleep(0.3)

    send_keys('^v')
    time.sleep(2)

    send_keys('{ENTER}')
    time.sleep(5)

def maximize_windows_with_title_substring(substring):
    def window_enum_callback(hwnd, data):
        title = win32gui.GetWindowText(hwnd)
        if substring in title:
            if not win32gui.IsWindowVisible(hwnd):
                return
            print(f"Maximizing window with title: {title}")
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    win32gui.EnumWindows(window_enum_callback, None)

if __name__ == "__main__":
    maximize_windows_with_title_substring("Zoom")
