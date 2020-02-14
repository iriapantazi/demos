#! /usr/bin/env python

import argparse
import requests
import json
import sys
import os
import datetime
import time
from colorama import Fore
import csv
import logging


# hard-coded values with information about the tfl API
TFLAPI = 'https://api.tfl.gov.uk'
HEADERS = {'Accept': 'application/json; charset=utf-8'}
SAVEFILE = 'output_lines_status.csv'
LOGFILE = 'lines_status.log'


def detect_python_version():
    """
    detect_python_version:
    Args: - 
    Returns: -
    """
    if sys.version_info.major < 3:
        msg = (f'Python {sys.version_info.major}.'
                f'{sys.version_info.minor} '
                f'is no more supported, hence the '
                f'program exits.')
        logging.critical(msg)
        sys.exit(-1)


def parse_arguments():
    """
    parse_arguments:
    Args: -
    Returns: args [str]
    This function includes the parser initialisation
    where all the valid arguments that can be parsed
    by the user are contained.
    """
    parser = argparse.ArgumentParser(
                description='This program prints the'
                ' train lines of London taken from the tfl API.'
                ' The valid modes that can be requested by the user'
                ' are only: tube, tram, dlr, tflrail,'
                ' overground. Use the flag -a for all modes, or'
                ' the flag -m followed by the desired mode(s).'
                ' With the flag -f the user can forces the request'
                ' even if not enough time has passed.')
    parser.add_argument('-m', '--modes', nargs='+', 
                help='entrer the train mode(s)')
    parser.add_argument('-a', '--all_modes', action='store_true',
                help='for tube lines, DLR, tram, tflrail, overground')
    parser.add_argument('-f', '--force', action='store_true',
                help='force request, and also include'
                'the desired mode(s)')
    parser.add_argument('-t', '--time_to_leave', nargs='?', 
                const='300', type=int, 
                help='perform request after these seconds')
    parser.add_argument('-o', '--output', nargs='?', 
                const='output_lines_status.csv', type=str, 
                help='perform request after these seconds')
    parser.add_argument('-l', '--logging_level', nargs='?', 
                const='WARNING', help='set the logging level')
    args = parser.parse_args()
    return(args)


def configure_logger(lvl):
    """
    configure_logger:
    Args: lvl [str]
    Returns: -
    This function configures the logger
    """
    log_lvl = getattr(logging, lvl)
    logging.basicConfig(filename=LOGFILE,
            level=log_lvl, filemode='w',
            format='%(asctime)s--%(levelname)s--%(message)s')


def check_last_time_executed_requests(ttl):
    """
    check_last_time_executed_requests:
    Args: - 
    Returns: toRequest [bool]
    This file checks the last time that a requests.get
    was sent to the server. If it was within 5 min
    the status will be read from the SAVEFILE.
    """
    toRequest = False
    nowTime = int(time.time())
    try:
        with open(SAVEFILE, 'r') as f:
            thenTime = int(f.readline())
            if (nowTime - thenTime > ttl):
                toRequest = True
    except FileNotFoundError as err:
        logging.warning(f'{err}: will request.')
        toRequest = True
    except ValueError as err:
        logging.warning(f'{err}: No valid format of {SAVEFILE}, '
                f'will be considered as FileNotFoundError.')
        toRequest = True
    except Exception as e:
        logging.critical(f'{e}: system exits: system exits.')
        sys.exit(-1)
    return(toRequest)


def associate_status_color(rowCode):
    """
    associate_status_color:
    Args: status [str]
    Return: clr [str]
    This function assigns colors in ANSI format
    for different line status.
    """
    rowCode = rowCode % 6
    colors = ['BLUE', 'CYAN', 'RED', 'MAGENTA', 'GREEN', 'YELLOW']
    color = colors[rowCode]
    try:
        clr = getattr(Fore, color)
    except Exception as e:
        logging.error(f'Error with the color attributes: {e}')
        clr = getattr(Fore, 'RESET')
    else:
        return(clr)


def print_saved_data():
    """
    print_saved_data:
    Args: - 
    Returns: -
    This function reads from SAVEFILE the name(s)
    and the status of each line and prints to the
    standard output.
    """
    with open(SAVEFILE, 'r') as f:
        # to skip 1st line that includes timestamp
        time = f.readline()
        f_reader = csv.reader(f, delimiter=',') 
        for row in f_reader:
            try:
                rowName = row[0]
                rowCode = int(row[1])
                rowDesc = row[2]
                clr = associate_status_color(rowCode)
            except Exception as e:
                logging.error(e)
                sys.exit(-1)
            else:
                print(f'{rowName} Line reports {clr} '
                        f'{rowDesc} {Fore.RESET}')


def request_status_from_server(url):
    """
    request_status_from_server:
    Args: url [string]
    Returns: data [list]
    This module will request information
    on lines status and will return then
    in the form of list contaning a dictionary.
    """
    r = requests.get(url, headers=HEADERS)
    if not r.ok:
        msg = (f'Exits with request status code '
                f'{r.status_code} on {url}.')
        logging.critical(msg)
        sys.exit(-1)
    data = r.json()
    if (type(data) != list or len(data) < 1):
        msg = (f'request_status_from_server: '
                f'Received not list, or empty list. '
                f'Aborting.')
        logging.critical(msg)
        sys.exit(-1)
    return(data)


def get_dictionary_key(theDict, theKey):
    """
    get_dictionary_key:
    Args: theDict [dict], theKey [str]
    Returns: ?
    This function asserts that the key exists
    in the dictionary, and returns the value. 
    If it does not, it logs an error and exits
    with the appropriate message.
    """
    try: 
        theValue = theDict.get(theKey)
    except KeyError:
        msg = f'Dictionary {theDict} contains no key {theKey}.'
        logging.error(msg)
        sys.exit(-1)
    else:
        return(theValue)


def write_save_data(data):
    """
    write_save_data:
    Args: data [list]
    Returns: -
    This function opens a file where the output will 
    be written, and saves the line name, status code,
    and status message as comma separated values.
    """
    with open(SAVEFILE, 'w') as f:
        nowTime = int(time.time())
        f.write(f'{nowTime}\n')

        if type(data) != list: 
            logging.error(f'Expected {data} to be a list.')
            sys.exit(-1)

        for status in data:
            if (type(status) != dict):
                logging.error(f'Expected {status} to be a dictionary.')
                sys.exit(-1)
            lineName = get_dictionary_key(status, 'name')
            lineStatus = get_dictionary_key(status, 
                    'lineStatuses')[0]
            statusCode = get_dictionary_key(lineStatus, 
                    'statusSeverity')
            statusDescription = get_dictionary_key(lineStatus, 
                    'statusSeverityDescription')
            f.write(f'{lineName},{statusCode},{statusDescription}\n')


def create_status_URL(modes):
    """
    create_status_URL:
    Args: modes [str]
    Returns: url [str]
    This function generates the appropriate url for
    requesting the status of valid modes.
    """
    try:
        url = f'{TFLAPI}/line/mode/{modes}/status'
    except Exception as e:
        logging.error(e)    
        sys.exit(-1)
    else:
        return(url)


def return_valid_modes_string(modes):
    """
    return_valid_modes_string:
    Args: modes [str]
    Returns: request_modes [str]
    correction to accelerate testing of the modes
    validity. so that it rejects non-valid or
    non-implemented modes.
    """
    request_modes = []
    if 'tube' in modes:
        request_modes.append('tube')
    if 'overground' in modes:
        request_modes.append('overground')
    if 'tflrail' in modes:
        request_modes.append('tflrail')
    if 'tram' in modes:
        request_modes.append('tram')
    if 'dlr' in modes:
        request_modes.append('dlr')
    if (len(request_modes) < 1 or type(request_modes) != list):
        logging.error(f'returnValidModesString: '
                f'received no valid modes. Aborting.')
        sys.exit(-1)
    request_modes = ','.join(request_modes)
    return(request_modes)


def return_all_valid_modes_string():
    """
    return_all_valid_modes_string:
    Args: - 
    Returns: request_modes [str]
    This is hard coded to include only
    dlr, tram, tube, overgound, tflrail.
    """
    request_modes = (f'tube,tram,overground,dlr,tflrail')
    return(request_modes)


def execute_request(ttl, toRequest, modes, all_modes):
    """
    execute_request:
    Args: -
    Returns: -
    """
    if toRequest:
        try:
            if all_modes:
                modesString = return_all_valid_modes_string()
            else:
                modesString = return_valid_modes_string(modes)
        except Exception as e:
            logging.error(e)
            sys.exit(-1)

        statusURL = create_status_URL(modesString)
        data = request_status_from_server(statusURL)
        write_save_data(data)

    else:
        logging.warning(f'No request since less than {ttl} '
                f'seconds have passed. Reads output from file.')



def main():
    """
    main:
    Args: -
    Returns: -
    This function includes all the calls to methods 
    where each one of them has a specific functionality.
    """

    # parse arguments
    args = parse_arguments()

    # logging level
    if args.logging_level:
        lvl = args.logging_level
    else:
        lvl = 'WARNING'
    configure_logger(lvl)

    # detect python version
    detect_python_version()

    # time to leave
    if args.time_to_leave:
        ttl = args.time_to_leave
    else:
        ttl = 300

    # force request
    if args.force:
        toRequest = args.force
    else:
        toRequest = check_last_time_executed_requests(ttl)

    # execute request
    if args.all_modes:
        modes = args.all_modes
    elif args.modes:
        modes = args.modes
    else:
        msg = (f'No modes option found.'
               f'See help for valid modes.')
        logging.critical(msg)
        sys.exit(-1)
    execute_request(ttl, toRequest, modes, args.all_modes)

    # store data
    print_saved_data()

if __name__ == "__main__":
    main()
