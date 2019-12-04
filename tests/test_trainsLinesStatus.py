#! /usr/bin/env python 

import unittest
from unittest.mock import Mock, patch
import tfl_requests
import tfl_requests.trainsLinesStatus as tls
from tfl_requests.trainsLinesStatus import SAVEFILE, TFLAPI
from colorama import Fore
import datetime
import sys

class Testing(unittest.TestCase):
    """
    Testing: class that calls the functions
    of the program trainsLinesStatus.py
    """

    def test_detectPythonVersion(self):
        """
        test_detectPythonVersion:
        Test if python version is supported.
        """
        tls.detectPythonVersion()

        patcher = patch('sys.version_info', major=2, minor=7)
        patcher.start()
        with self.assertRaises(Exception): 
            tls.detectPythonVersion()

    def test_checkLastTimeExecutedRequests(self):
        """
        test_checkLastTimeExecutedRequests: 
        Test of the function determining whether
        a new request is necessary.
        """
        returned = tls.checkLastTimeExecutedRequests()
        patcher = patch('tfl_requests.trainsLinesStatus.'
                'checkLastTimeExecutedRequests', True)
        patcher.start()
        #self.assertEqual(returned, True)


    def test_associateStatusColor(self):
        """
        test_associateStatusColor:
        Test of the function assigning
        a color to a line status code.
        """
        colors = ['BLUE', 'CYAN', 'RED', 
                'MAGENTA', 'GREEN', 'YELLOW']
        colors = [getattr(Fore, i) for i in colors]
        for i in range(0, 100):
            returned = tls.associateStatusColor(i)
            expected = colors[i % 6]
            self.assertEqual(returned, expected)


    def test_printFormattedData(self): 
        """
        test_printFormattedData:
        Test of the function responsible
        for printing entries of a file
        to the terminal.
        """
        #tls.printFormattedData()
        #mock = Mock()
        #print = mock
        #mock.tls.printFormattedData()
        #list_status = ['Good Service', 'Minor Delays', 
        #               'Severe Delays', 'Planned Closure',
        #               'Part Closure', 'Part Suspended', 'bar']
        #list_colors = [Fore.CYAN, Fore.RED,
        #               Fore.GREEN, Fore.YELLOW,
        #               Fore.MAGENTA, Fore.GREEN, Fore.BLUE]
        #for s, c in zip(list_status, list_colors):
        #    mock.tls.printFormattedData()  
        #    #expected = 'Line reports '+ c + s + '\033[0m'
        #    #self.assertEqual(returned, expected)


    def test_requestStatusFromServer(self):
        """
        test_requestStatusFromServer:
        Tests whether a request is performed, 
        and data are received. 
        """
        with patch('tfl_requests.trainsLinesStatus.'
                'requestStatusFromServer') as mock_get:
            expected =  '' 
            mock_get.return_value.data = expected
            returned = tls.requestStatusFromServer('')
        #self.assertEqual(expected, returned)


    def test_writeAndSaveData(self):
        """
        test_writeAndSaveData:
        Tests whether a file opens, and the
        requested data are written as comma
        separated values.
        """
        sample_data = [
                {'name': 'a_name', 
                'lineStatuses': [
                    {'statusSeverity': '0',
                    'statusSeverityDescription': 'ok'}]
                }]
        tls.writeAndSaveData(sample_data)
        #self.assertEqual()


    def test_createStatusURL(self):
        """
        test_createStatusURL:
        Tests whether the appropriate url
        is created, and returns it.
        """
        returned = tls.createStatusURL('k')
        expected = '{}/line/mode/{}/status'.format(TFLAPI, 'k')
        self.assertEqual(returned, expected)


    def test_returnValidModesString(self):
        """
        test_returnValidModesString:
        Tests whether the arguments parsed 
        are valid.
        """


    def test_returnValidAllModesString(self):
        """
        test_returnValidAllModesString:
        """



if __name__=='__main__':
    unittest.main()
