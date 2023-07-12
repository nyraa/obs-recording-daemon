from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyperclip


def launch_cmd(cmd):
    send_keys('{LWIN down}r{LWIN up}')
    run = Application().connect(title='執行', timeout=5)
    pyperclip.copy(cmd)
    run.執行.type_keys('^v{ENTER}')