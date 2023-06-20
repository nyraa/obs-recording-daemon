import configparser
import datetime
import logging

import actions

logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(module)s - %(message)s')

logger = logging.getLogger(__name__)

logger.info('=== Round started ===')

config = configparser.ConfigParser()
config.read('config.ini')

state = config['DEFAULT']['state']
running = config['DEFAULT']['running']
remove_expired = config['DEFAULT'].getboolean('remove_expired')
entry_to_remove = []


for entry in config:
    if entry == 'DEFAULT':
        continue
    try:
        logger.info(f'Checking entry [{entry}]')
        start = config[entry]['start']
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end = config[entry]['end']
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        keep = config.getboolean(entry, 'keep')

        # check start < end
        if start_date > end_date:
            logger.warning(f'Start date is after end date [{entry}]')
            print('start date is after end date', entry)
            continue

        # if end is in the past, and running is current entry, then we need to stop the daemon
        if end_date < datetime.datetime.now() and running == entry:
            logger.info(f'Stop task [{entry}]')
            print('stop task', entry)
            actions.stop_recording(config[entry])
            config.set('DEFAULT', 'running', '')
            config.set('DEFAULT', 'state', 'idle')
        # if start date is in the past, then we need to start the daemon
        elif start_date < datetime.datetime.now() and end_date > datetime.datetime.now() and state == 'idle':
            logger.info(f'Start task [{entry}]')
            print('start task', entry)
            actions.start_recording(config[entry])
            config.set('DEFAULT', 'running', entry)
            config.set('DEFAULT', 'state', 'running')
            continue
        if remove_expired and end_date < datetime.datetime.now() and not keep:
            logger.info(f'Entry [{entry}] expired')
            entry_to_remove.append(entry)
    except KeyError:
        logger.warning(f'Invalid config entry [{entry}]')
        continue

logger.info('Removing expired entries...')
for entry in entry_to_remove:
    logger.info(f'removing entry [{entry}]')
    config.remove_section(entry)

logger.info('Saving config...')
with open('config.ini', 'w') as configfile:
    config.write(configfile)

logger.info('=== Round finished ===')