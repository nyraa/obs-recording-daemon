from obswebsocket import obsws, requests
import configparser
import logging

import urllib.parse
import os
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyperclip

import time

logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s - %(message)s')

logger = logging.getLogger(__name__)

client = None
scene = None

def init():
    logger.info('Init obs socket')
    obs_config = configparser.ConfigParser()
    obs_config.read('obs_config.ini', encoding='utf-8')
    host = obs_config['DEFAULT']['host']
    port = obs_config['DEFAULT']['port']
    logger.info(f'Connecting to obs websocket {host}:{port}')
    password = obs_config['DEFAULT']['password']
    global scene
    scene = obs_config['DEFAULT']['scene']

    global client
    client = obsws(host, port, password)
    client.connect()
        

def destroy():
    global client
    if client is None:
        return
    client.disconnect()

def start_recording(entry):
    if client is None:
        try:
            init()
        except:
            logger.warning('OBS maybe not running, try to launch OBS')
            launch_cmd(r"C:\Program Files\obs-studio\bin\64bit\obs64.exe")
            time.sleep(10)
            try:
                init()
            except:
                logger.error('OBS launching retry failed')
                return False


    logger.info('Launching zoom')
    try:
        room_id = entry['room']
        password = entry['password']
        name = entry['name']
        
        logger.info(f'Room id: {room_id}, Password: {password}, Name: {name}')
        launch_cmd(rf'%appdata%\Zoom\bin\Zoom.exe "--url=zoommtg://zoom.us/join?action=join&confno={room_id}&pwd={password}&uname={urllib.parse.quote_plus(name)}"')

        zoom = Application(backend='uia').connect(title='Zoom', timeout=60)
        zoom.Zoom.type_keys('{ESC}')

    except Exception as e:
        logger.error(e)
        print(e)
        return False
    logger.info('Zoom started')
    print('start recording', entry)
    logger.info('Start recording')
    try:
        client.call(requests.StartRecord())
    except Exception as e:
        logger.error(e)
        print(e)
        return False
    return True

def stop_recording(entry):
    if client is None:
        try:
            init()
        except:
            logger.error('Can not connect to OBS when stop recording')
    print('stop recording', entry)
    logger.info('Stop recording')
    try:
        res = client.call(requests.StopRecord())
    except:
        logger.warning('OBS call StopRecord failed')
    
    # terminate Zoom
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

    # save OBS output
    if len(res.datain) == 0:
        logger.warning('No outputPath in the response, recording maybe failed')
        return False
    else:
        file_path = res.datain['outputPath']
        logger.info(f'Save the recording file to path: {file_path}')
        return True

def launch_cmd(cmd):
    send_keys('{LWIN down}r{LWIN up}')
    run = Application().connect(title='執行', timeout=5)
    pyperclip.copy(cmd)
    run.執行.type_keys('^v{ENTER}')