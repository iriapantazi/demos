#! /usr/bin/env python

import argparse
import requests
import json
import sys
import os
import datetime
import colorama
from colorama import Fore
import pandas as pd

parser = argparse.ArgumentParser(
            description="This program prints the\
            train lines, i.e. tube, dlr, tram, overground\
            of London at the time that the program is executed.\
            The valid modes are only: tube, tram, dlr,\
            overground. Enter the desired one(s) after the\
            flag -m.")
parser.add_argument('-m', '--modes', nargs='+', 
                    help='entrer the train mode(s)')
parser.add_argument('-a', '--all_modes', action='store_true',
                    help='for tube lines, DLR, tram, overground')
parser.add_argument('-f', '--force', action='store_true',
                    help='force request, and also include'
                    'the desired modes to')
args = parser.parse_args()


TFLAPI = 'https://api.tfl.gov.uk'
HEADERS = {'Accept': 'application/json; charset=utf-8'}
SAVEFILE = 'outputLinesStatus.csv'


def detectPythonVersion():
    """
    detectPythonVersion: Args: - Returns: -
    This module checks if the user 
    has joined reality by raising Exception
    if they are using Python2.x.
    """
    if sys.version_info[0] < 3:
        message = 'Python' + str(sys.version_info[0]) +\
                  '.x is about to retire. ' +\
                  'Please join reality and update.'
        raise Exception(message)


def checkLastTimeExecutedRequests():
    """
    checkLastTimeExecutedRequests: Args: - Returns: -
    This file checks the last time that a requests.get
    was sent to the server, and if it was within 10 min
    then, the file that keeps the status for each line
    will be called, and the information will be printed
    on the terminal. If 10 minutes have passed, then a
    new request will be sent to the server.
    """
    toRequest = False
    nowDate, nowTime = getDateTimeFormatted()
    #print(nowDate)
    #print(nowTime)
    try:
        with open(SAVEFILE, 'r') as f:
            line = f.readline()
            thenDate, thenTime = line.split(',')
            #print(thenDate)
            #print(thenTime)
            if (nowDate != thenDate):
                print('Detected different date. Will request.')
                toRequest = True
            else:
                toRequest = compareTime(thenTime, nowTime)
    except FileNotFoundError:
        print('no file found, will request')
        toRequest = True
    except:
        print('something went wrong.')
        sys.exit(-1)
    if (os.path.getsize(SAVEFILE) < 1):
        toRequest = True
    return(toRequest)


def getDateTimeFormatted():
    nowTime = datetime.datetime.now()
    date = str('{}-{}-{}'.format(nowTime.year, nowTime.month, nowTime.day))
    time = str('{}:{}'.format(nowTime.hour, nowTime.minute))
    return(date, time)


def compareTime(thenTime, nowTime):
    thenHr, thenMin = thenTime.split(':')
    nowHr, nowMin = nowTime.split(':')
    #print(thenHr)
    #print(thenMin)
    #print(nowHr)
    #print(nowMin)
    if (thenHr != nowHr):
        print('Different hour, will request.')
        toRequest = True
    elif (int(nowMin) - int(thenMin) > 5):
        print('More than 5 min difference, will request.')
        toRequest = True
    else:
        print('No need to request. Not enough time passed.')
        toRequest = False
    return(toRequest)


def printFormattedData():
    """
    printFormattedData: Args: - Returns: -
    this function reads the csv file named SAVEFILE
    and the status of each line is printed with
    the appropriate color.
    """
    data = pd.read_csv(SAVEFILE, names = ['lineName', 'lineStatus'],
                       header = 0)
    for i in range(len(data)):
        tempName = data['lineName'][i]
        tempStat = data['lineStatus'][i]
        if (tempStat == 'Good Service'):
            clr = Fore.CYAN
        elif (tempStat == 'Minor Delays'):
            clr = Fore.RED
        elif (tempStat == 'Severe Delays'):
            clr = Fore.GREEN
        elif (tempStat == 'Planned Closure'):
            clr = Fore.YELLOW
        elif (tempStat == 'Part Closure'):
            clr = Fore.MAGENTA
        elif (tempStat == 'Part Suspended'):
            clr = Fore.GREEN
        else:
            clr = Fore.BLUE
        print(('{} Line reports ' + clr +\
              '{} \033[0m').format(tempName, tempStat))


def requestStatusFromServer(url):
    """
    requestStatusFromServer: Args: url [string]
    Returns: [list of dictionary]
    This module will request information
    on lines status and will return then
    in the form of list contaning a dictionary.
    """
    r = requests.get(url, headers=HEADERS)
    if not r.ok:
        print('Exits with request status code'
              '{} on {}.'.format(r.status_code, url))
        sys.exit(-1)
    data = r.json()
    if (type(data) != list or len(data) < 1):
        print('requestFromServer: Received not list,'
              'or empty list of status for lines, Aborting.')
        sys.exit(-1)
    return(data)


def writeAndSaveData(data):
    """
    """
    with open(SAVEFILE, 'w') as f:
        date, time = getDateTimeFormatted()
        f.write('{},{}\n'.format(date, time))
        for status in data:
            if (type(status) != dict):
                print('requestFromServer: contact me')
                sys.exit(-1)
            lineName = status.get('name')
            lineStatus = status.get('lineStatuses')[0]
            lineStatus = lineStatus.get('statusSeverityDescription')
            f.write('{},{}\n'.format(lineName, lineStatus))


def createStatusURL(modes):
    """
    include appropriate if checks
    the if statement below must have already
    been checked.
    """
    #if (not modes or modes == ""):
    #    print('createStatusURL: ')
    #    sys.exit(-1)
    #return("{}/line/mode/{}/status".format(TFLAPI, modes))
    try:
        url = '{}/line/mode/{}/status'.format(TFLAPI, modes)
    except:
        # include appropriate exception can include many except's
        # for each raised exception!!!
       pass
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
    if 'tram' in modes:
        request_modes.append('tram')
    if 'dlr' in modes:
        request_modes.append('dlr')
    if (len(request_modes) < 1 or type(request_modes) != list):
        print('returnValidModesString: received no valid modes.'
              ' Aborting.')
        sys.exit(-1)
    request_modes = ','.join(request_modes)
    return(request_modes)


def returnAllValidModesString():
    """
    returnAllValidModesString: Args: - 
    Returns: all valid train modes.
    This is hard coded to include only
    dlr, tram, tube, overgound.
    """
    request_modes = 'tube,tram,overground,dlr'
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
        print('No request. Reads output from file.')
    printFormattedData()


if __name__ == "__main__":
    main()
