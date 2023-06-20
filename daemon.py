import configparser
import datetime
import logging

logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

logging.info('round started')

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
        logging.info(f'checking entry [{entry}]')
        start = config[entry]['start']
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end = config[entry]['end']
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        keep = config.getboolean(entry, 'keep')

        # check start < end
        if start_date > end_date:
            logging.warning(f'start date is after end date [{entry}]')
            print('start date is after end date', entry)
            continue

        # if end is in the past, and running is current entry, then we need to stop the daemon
        if end_date < datetime.datetime.now() and running == entry:
            logging.info(f'stop task [{entry}]')
            print('stop task', entry)
            config.set('DEFAULT', 'running', '')
            config.set('DEFAULT', 'state', 'idle')
        # if start date is in the past, then we need to start the daemon
        elif start_date < datetime.datetime.now() and end_date > datetime.datetime.now() and state == 'idle':
            logging.info(f'start task [{entry}]')
            print('start task', entry)
            config.set('DEFAULT', 'running', entry)
            config.set('DEFAULT', 'state', 'running')
            continue
        if remove_expired and end_date < datetime.datetime.now() and not keep:
            logging.info(f'entry [{entry}] expired')
            entry_to_remove.append(entry)
    except KeyError:
        logging.warning(f'invalid config entry [{entry}]')
        continue

logging.info('removing expired entries...')
for entry in entry_to_remove:
    logging.info(f'removing entry [{entry}]')
    config.remove_section(entry)

logging.info('saving config...')
with open('config.ini', 'w') as configfile:
    config.write(configfile)

logging.info('round finished')