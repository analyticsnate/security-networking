import logging
import time
import json
import os
import shutil

# requires config.json file to execute

# TODO: clean up by removing duplicate config variables

def load_json(json_file):
    location = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    js_file = open(os.path.join(location, json_file))
    js_str = js_file.read()
    js_dict = json.loads(js_str)
    return js_dict

_config_ = load_json('config.json')

__datefmt__ = '%Y%m%d %I:%M:%S'
__now__ = str(int(time.time()))
__here__ = _config_['here']

_folder_check_ = _config_['custom_config_file']

_interface_from_ = _config_['interface_from']
_interface_to_ = _config_['interface_to']

_logfile_ = '{0}/logs/{1}_pi_hdd_check.log'.format(__here__, __now__)

logging.basicConfig(filename=_logfile_, filemode='w', level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt=__datefmt__)

logging.info('# PI HDD CHECK')

def end_process():
    os.remove(_logfile_)
    exit()

try:
    with open(_folder_check_, 'r') as f:
        custom_config = json.load(f)

    if custom_config['have_metawear_data']:
        logging.debug('-- have_metawear_data = True | downloading data and logs')
        logging.debug('_interface_from_ ' + _interface_from_)
        logging.debug('_interface_to_ ' + _interface_to_)
        logging.info('# BEGINNING TRANSFER')

        # transfer data files
        data_file_count = 0
        for f in os.listdir(_interface_from_ + 'data'):
            # only transfer .csv files
            if f[-3:] == 'csv':
                file_from = _interface_from_ + 'data/' + f
                file_to = _interface_to_ + 'data/' + f

                shutil.move(file_from, file_to)                
                logging.debug(f + ' transfer complete')
                data_file_count += 1

        logging.info('# {0} DATA FILES TRANSFERRED'.format(data_file_count))

        # transfer log files
        log_file_count = 0
        for f in os.listdir(_interface_from_ + 'logs'):
            # only transfer .log files
            if f[-3:] == 'log':
                file_from = _interface_from_ + 'logs/' + f
                file_to = _interface_to_ + 'logs/' + f
                    
                shutil.move(file_from, file_to)
                logging.debug(f + ' transfer complete')
                log_file_count += 1

        logging.info('# {0} LOG FILES TRANSFERRED'.format(log_file_count))

        # set have_metawear_data to false
        custom_config['have_metawear_data'] = False
        with open(_folder_check_, 'w') as fp:
            json.dump(custom_config, fp)
            logging.debug('-- have_metawear_data set to False')

        logging.info('# PI HDD CHECK closing')

except FileNotFoundError as err:
    # this error generally occurs when the micro-SD card is not present
    end_process()