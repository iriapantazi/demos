#! /usr/bin/python 

import argparse
import requests
import json
import sys
from colorama import Fore, Back, Style

parser = argparse.ArgumentParser(description=' This program prints the train lines\
            (i.e. tube, dlr, tram, overground) of London at \
            the time that the program is executed.', \
            epilog='The program is still under construction. \
            Currently only tube lines are available. \
            There is only the option of getting the status \
            all lines, and not choose specific ones.')
parser.add_argument('-m', '--tram', action='store_true', help='look only for tram lines')
parser.add_argument('-t', '--tube', action='store_true', help='look only for tube lines')
parser.add_argument('-d', '--dlr', action='store_true', help='look only for dlr lines')
parser.add_argument('-o', '--overground', action='store_true', help='look only for overground lines')
args = parser.parse_args()

TFLAPI = 'https://api.tfl.gov.uk'
HEADERS = {'Accept':'application/json; charset=utf-8'}



def getLineIDs(data):
    """
    getLineNames: 
    Input: data, which is a list of size equal to 11.
    Returns: a comma separated string csNames.
    Each list entry contains a dictionary, and for the 
    key 'id', the value is the line name, e.g. victoria.
    The string csNames contains all the tube lines names 
    extracted from the list entries in the form 
    victoria,circle,hammersmith-city,... etc.
    It is used the 'id' key instead of the 'name' key.
    """
    csNames = [cs.get('id') for cs in data]
    # Here I want to insert a test for the type 
    # of the list entries, and the existence of such lines.
    if  type(csNames) != list or len(csNames) < 1 or csNames == ['']:
        print('getLineIDs: did not get any valid tube line names. Aborting.')
        sys.exit(-1)
    csNames = ",".join(csNames)
    return(csNames)

def getTubeLinesNames(modeName): 
    """
    getTubeLinesNames: 
    Args: the URL for the tube mode.
    Returns: the names of the tube lines.
    Tube lines names are requested from constant TFLAPITUBE.
    The response is in JSON format, and it is
    a list of size 11, as are the different lines.
    Each list entry contains a dictionary 
    with info about the line.
    """
    r = requests.get(modeName, headers=HEADERS)
    if not r.ok :
        print('Exits with request status code {} on {}.'.format(r.status_code, TFLAPITUBE))
        sys.exit(-1)
    data = r.json()
    if (type(data) != list or len(data) < 1) :
        print('getTubeLines: Request returned not list, or empty list of line names. Aborting.')
        sys.exit(-1)
    lineNames = getLineIDs(data)
    return(lineNames)

def tubeStatusURL(lineNames):
    """
    tubeStatusURL: Args: comma separated lines names string.
    Returns: the appropriate url for the API that 
    contains the status for all the tube lines.
    """
    if (not lineNames or lineNames =="") :
        print('tubeStatusURL: ')
        sys.exit(-1)
    return("{}/Line/{}/Status".format(TFLAPI, lineNames))

def getTubeStatus(lineNames):
    """ 
    getTubeStatus: Args: comma separated line names string.
    Returns: -
    Thie module request the status of all the tube lines.
    The response is a list of size 11 for all the lines. 
    Each list entry contains a distionary, and for the 
    key 'lineStatuses', the value is another list of size 1 
    that contains a dictionary. In that dictionary, the 
    key 'statusSeverityDescription' has the value of 
    the line status, e.g. 'Good Service', 'Planned Closure', 
    'Part Closure', 'Part Suspended', 'Minor Delays', etc.
    """
    url = tubeStatusURL(lineNames)
    r = requests.get(url, headers=HEADERS)
    if not r.ok :
        print('Exits with request status code {} on {}.'.format(r.status_code, TFLAPI))
        sys.exit(-1)
    data = r.json()
    if (type(data) != list or len(data) < 1) :
        print('getTubeStatus: Received not list, or empty list of status for lines, Aborting.')
        sys.exit(-1)
    for status in data:
        if (type(status) != dict ) :
            print('getTubeStatus: did not receive dict type. Contact me.')
            sys.exit(-1)
        lineName = status.get('name')
        lineStatus = status.get('lineStatuses')[0]
        lineStatus = lineStatus.get('statusSeverityDescription')
        statusPrint = printTubeNameStatusFormatted(lineName, lineStatus)
        print(statusPrint)


def printTubeNameStatusFormatted(lineName, lineStatus):
    """ 
    printTubeNameStatusFormatted: Args: string lineName, and string lineStatus
    Returns: The formatted string that will be printed in the terminal.
    The format has a different color for the various status.
    """
    if (lineStatus == 'Good Service'):
        clr = Fore.CYAN
    elif (lineStatus == 'Minor Delays'):
        clr = Fore.RED
    elif (lineStatus == 'Planned Closure'):
        clr = Fore.YELLOW
    elif (lineStatus == 'Part Closure'):
        clr = Fore.MAGENTA
    elif (lineStatus == 'Part Suspended'):
        clr = Fore.GREEN
    else:
        clr = Fore.BLUE 
    return(('Line {} reports '+clr+'{}'+'\033[0m').format(lineName, lineStatus))

def printModeStatus(modeName):
    """
    printModeStatus: The function that 
    """
    lineNames = getTubeLinesNames(modeName)
    getTubeStatus(lineNames)

def main():
    """ 
    main: Args: the arguments that are parsed from the terminal. 
    The appropriate arguments are described through the command 
    "./trainsLinesStatus.py --help"
    If they are not correct, then the program prints an error message 
    and exits.
    According to the argument parsed, the appropriate functions are 
    called. For instance, tube has multiple line names, whereas the 
    the rest of the modes (tram, overground, dlr) are single lines.
    """
    if len(sys.argv) < 2 :
        print('ERROR: Please supply a valid argument for train mode. Aborting.')
        sys.exit(-1)
    elif (args.tube):
        modeName = TFLAPI + '/Line/Mode/tube'
        printModeStatus(modeName)
    elif (args.dlr):
        modeName = TFLAPI + '/line/dlr/status'
        print('ERROR: not yet implemented dlr lines.')
        sys.exit(-1)
    elif (args.tram):
        modeName = TFLAPI + '/line/tram/status'
        print('ERROR: not yet implemented tram lines.')
        sys.exit(-1)
    elif (args.overground):
        modeName = TFLAPI + '/line/dlr/status'
        print('ERROR: not yet implemented London overground lines.')
        sys.exit(-1)
    else :
        print('ERROR: please provide a valid train mode type. See help for the \
                valid modes. Aborting.')
        sys.exit(-1)

if __name__ == "__main__":
    main()


