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

parser = argparse.ArgumentParser(
            description="This program prints the"
            " train lines, i.e. tube, dlr, tram, overground"
            " of London at the time that the program is executed."
            " The valid modes are only: tube, tram, dlr,"
            " overground. Enter the desired one(s) after the"
            " flag -m, or use -a for all modes. Flag -f forces"
            " the request even if not enough time has passed.")
parser.add_argument('-m', '--modes', nargs='+', 
                    help='entrer the train mode(s)')
parser.add_argument('-a', '--all_modes', action='store_true',
                    help='for tube lines, DLR, tram, overground')
parser.add_argument('-f', '--force', action='store_true',
                    help='force request, and also include'
                    'the desired mode(s)')
args = parser.parse_args()

logging.basicConfig(filename='tfl_requests.log',
        filemode='w',
        format='%(asctime)s--%(levelname)s--%(message)s')

TFLAPI = 'https://api.tfl.gov.uk'
HEADERS = {'Accept': 'application/json; charset=utf-8'}
SAVEFILE = 'outputLinesStatus.csv'


def detectPythonVersion():
    """
    detectPythonVersion: 
    Args: - 
    Returns: -
    """
    if sys.version_info.major < 3:
        message = 'Python' + str(sys.version_info.major) +\
                  str(sys.version_info.minor) +\
                  ' is retired or about to retire. ' +\
                  'Please update.'
        raise Exception(message)


def checkLastTimeExecutedRequests():
    """
    checkLastTimeExecutedRequests: 
    Args: - 
    Returns: -
    This file checks the last time that a requests.get
    was sent to the server. If it was within 5 min
    the status will be read from the SAVEFILE.
    """
    toRequest = False
    nowTime = int(time.time())
    try:
        with open(SAVEFILE, 'r') as f:
            thenTime = int(f.readline())
            if (nowTime - thenTime > 300):
                toRequest = True
    except FileNotFoundError as err:
        logging.warning('No file found, will request.')
        toRequest = True
    except ValueError as err:
        logging.warning('No valid format of SAVEFILE, '
                'will be considered as FileNotFoundError.')
        toRequest = True
    except Exception as e:
        loggind.error(e)
        print(e)
        print('Aborting.')
        sys.exit(-1)
    return(toRequest)


def associateStatusColor(rowCode):
    """
    associateStatusColor:
    Args: status [str]
    Return: clr [str]
    This function assigns colors in ANSI format
    for different line status.
    """
    colors = ['BLUE', 'CYAN', 'RED', 'MAGENTA', 'GREEN', 'YELLOW']*4
    color = colors[rowCode]
    clr = getattr(Fore, color)
    return(clr)


def printFormattedData():
    """
    printFormattedData: 
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
            rowName = row[0]
            rowCode = row[1]
            rowDesc = row[2]
            clr = associateStatusColor(int(rowCode))
            print(('{} Line reports ' + clr +\
                    '{}' + Fore.RESET).format(rowName, rowDesc))


def requestStatusFromServer(url):
    """
    requestStatusFromServer: 
    Args: url [string]
    Returns: data [list]
    This module will request information
    on lines status and will return then
    in the form of list contaning a dictionary.
    """
    r = requests.get(url, headers=HEADERS)
    if not r.ok:
        logging.error('Exits with request status code'
              '{} on {}.'.format(r.status_code, url))
        sys.exit(-1)
    data = r.json()
    if (type(data) != list or len(data) < 1):
        logging.error('requestFromServer: Received not list,'
              'or empty list of status for lines, Aborting.')
        sys.exit(-1)
    return(data)


def writeAndSaveData(data):
    """
    """
    with open(SAVEFILE, 'w') as f:
        nowTime = int(time.time())
        f.write('{}\n'.format(nowTime))
        for status in data:
            if (type(status) != dict):
                logging.error('requestFromServer: contact me')
                sys.exit(-1)
            lineName = status.get('name')
            lineStatus = status.get('lineStatuses')[0]
            statusCode = lineStatus.get('statusSeverity')
            statusDescription = lineStatus.get('statusSeverityDescription')
            f.write('{},{},{}\n'.format(lineName, statusCode, statusDescription))


def createStatusURL(modes):
    """
    include appropriate if checks
    the if statement below must have already
    been checked.
    """
    try:
        url = '{}/line/mode/{}/status'.format(TFLAPI, modes)
    except Exception as e:
        logging.error(e)    
    return(url)


def returnValidModesString(modes):
    """
    returnValideModesString:
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
        logging.warning('returnValidModesString: received no valid modes.'
              ' Aborting.')
        sys.exit(-1)
    request_modes = ','.join(request_modes)
    return(request_modes)


def returnAllValidModesString():
    """
    returnAllValidModesString: 
    Args: - 
    Returns: all valid train modes.
    This is hard coded to include only
    dlr, tram, tube, overgound.
    """
    request_modes = 'tube,tram,overground,dlr,tflrail'
    return(request_modes)


def main():
    """
    """
    detectPythonVersion()
    if (args.force):
        toRequest = True
    else:
        toRequest = checkLastTimeExecutedRequests()
    if toRequest:
        if (args.modes):
            modesString = returnValidModesString(args.modes)
        elif (args.all_modes):
            modesString = returnAllValidModesString()
        else:
            parser.print_help()
            sys.exit(-1)
        statusURL = createStatusURL(modesString)
        data = requestStatusFromServer(statusURL)
        writeAndSaveData(data)
    else:
        logging.warning('No request. Reads output from file.')
    printFormattedData()


if __name__ == "__main__":
    main()
