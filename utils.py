from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyperclip
import time


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