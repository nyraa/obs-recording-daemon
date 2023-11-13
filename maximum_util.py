
import win32gui
import win32con
import sys

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
    if len(sys.argv) > 1:
        maximize_windows_with_title_substring(sys.argv[1])
