#! /usr/bin/env python

import argparse
import requests
import json
import sys
import colorama
from colorama import Fore #, Back, Style

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
                    help='not implemented - inefficiency')
args = parser.parse_args()

TFLAPI = 'https://api.tfl.gov.uk'
HEADERS = {'Accept': 'application/json; charset=utf-8'}


#def getLineIDs(data):
#    """
#    getLineNames:
#    Input: data, which is a list of size equal to 11.
#    Returns: a comma separated string csNames.
#    Each list entry contains a dictionary, and for the
#    key 'id', the value is the line name, e.g. victoria.
#    The string csNames contains all the tube lines names
#    extracted from the list entries in the form
#    victoria,circle,hammersmith-city,... etc.
#    It is used the 'id' key instead of the 'name' key.
#    """
#    csNames = [cs.get('id') for cs in data]
#    if type(csNames) != list or len(csNames) < 1 or csNames == ['']:
#        print('getLineIDs: did not get any valid tube line names. Aborting.')
#        sys.exit(-1)
#    csNames = ",".join(csNames)
#    return(csNames)
#
#
#def getTubeLinesNames(modeName):
#    """
#    getTubeLinesNames:
#    Args: the URL for the tube mode.
#    Returns: the names of the tube lines.
#    Tube lines names are requested from constant TFLAPITUBE.
#    The response is in JSON format, and it is
#    a list of size 11, as are the different lines.
#    Each list entry contains a dictionary
#    with info about the line.
#    """
#    r = requests.get(modeName, headers=HEADERS)
#    if not r.ok:
#        print('Exits with request status code'
#              '{} on {}.'.format(r.status_code, TFLAPITUBE))
#        sys.exit(-1)
#    data = r.json()
#    if (type(data) != list or len(data) < 1):
#        print('getTubeLines: Request returned not list,'
#              'or empty list of line names. Aborting.')
#        sys.exit(-1)
#    lineNames = getLineIDs(data)
#    return(lineNames)
#
#
#def tubeStatusURL(lineNames):
#    """
#    tubeStatusURL: Args: comma separated lines names string.
#    Returns: the appropriate url for the API that
#    contains the status for all the tube lines.
#    """
#    if (not lineNames or lineNames == ""):
#        print('tubeStatusURL: ')
#        sys.exit(-1)
#    return("{}/Line/{}/Status".format(TFLAPI, lineNames))


