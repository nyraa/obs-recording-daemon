from pywinauto.application import Application
import urllib.parse
import logging
import os
import utils

logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s - %(message)s')
logger = logging.getLogger(__name__)


def hold_meeting():
    pass

def join_meeting(room_id, password, name):
    utils.launch_cmd(rf'%appdata%\Zoom\bin\Zoom.exe "--url=zoommtg://zoom.us/join?action=join&confno={room_id}&pwd={password}&uname={urllib.parse.quote_plus(name)}"')

    zoom = Application(backend='uia').connect(title='Zoom', timeout=60)
    zoom.Zoom.type_keys('{ESC}')

def terminate_meeting():
    try:
        zoom = Application(backend='uia').connect(title='Zoom', timeout=100)
        zoom.Zoom.type_keys('%{F4}')

        quit_dialog = Application(backend='uia').connect(title='結束會議或離開會議？', timeout=20)
        quit_btn = quit_dialog.結束會議或離開會議.child_window(title="離開會議", control_type="Button").wrapper_object()
        quit_btn.click_input()
    except Exception as e:
        logger.error(e)
    finally:
        os.system('TASKKILL /F /IM zoom.exe')