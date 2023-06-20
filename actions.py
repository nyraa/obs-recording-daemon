from obswebsocket import obsws, requests
import configparser
import logging

logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s - %(message)s')

logger = logging.getLogger(__name__)

client = None
scene = None


def init():
    logger.info('init obs socket')
    obs_config = configparser.ConfigParser()
    obs_config.read('obs_config.ini')
    host = obs_config['DEFAULT']['host']
    port = obs_config['DEFAULT']['port']
    logger.info(f'connecting to obs websocket {host}:{port}')
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
        init()
    print('start recording', entry)
    logger.info('start recording')
    client.call(requests.StartRecord())

def stop_recording(entry):
    if client is None:
        init()
    print('stop recording', entry)
    logger.info('stop recording')
    res = client.call(requests.StopRecord())
    file_path = res.datain['outputPath']