#! /usr/bin/env python 

import unittest
from unittest.mock import Mock, patch
import trainsLinesStatus as tls
from trainsLinesStatus import TFLAPI, HEADERS, SAVEFILE
from colorama import Fore
import sys

class Testing(unittest.TestCase):
    """
    Testing: class that calls the functions
    of the program trainsLinesStatus.py
    """
    def test_detectPythonVersion(self):
        """
        test_detectPythonVersion: to test
        if python version is supported.
        TODO
        """
        mock = Mock()

    def test_checkLastTimeExecutedRequests(self):
        """
        test_checkLastTimeExecutedRequests: 
        for the function that determines whether
        a new request is necessary.
        TODO
        """
        returned = tls.checkLastTimeExecutedRequests()
        possible = [True, False]
        if returned in possible:
            print('ok')


    def test_getDateTimeFormatted(self):
        """
        test_getDateTimeFormatted:
        TODO
        """
        returned = tls.getDateTimeFormatted()


    def test_compareTime(self):
        """
        test_compareTime: will check whether
        the criteria for requesting are the
        correct ones.
        TODO: mock printing
        """
        thenTime_list = ['1:0', '1:0', '1:0']
        nowTime_list = ['1:0', '1:4', '2:0']
        expected_list = [False, False, True]
        for then, now, expe in zip(thenTime_list, nowTime_list, expected_list):
            returned = tls.compareTime(then, now) 
            expected = expe
            self.assertEqual(returned, expected)


    def test_printFormattedData(self): 
        """
        test_printFormattedData:
        """
        mock = Mock()
        print = mock
        mock.tls.printFormattedData()
        list_status = ['Good Service', 'Minor Delays', 
                       'Severe Delays', 'Planned Closure',
                       'Part Closure', 'Part Suspended', 'bar']
        list_colors = [Fore.CYAN, Fore.RED,
                       Fore.GREEN, Fore.YELLOW,
                       Fore.MAGENTA, Fore.GREEN, Fore.BLUE]
        for s, c in zip(list_status, list_colors):
            mock.tls.printFormattedData()  
            #expected = 'Line reports '+ c + s + '\033[0m'
            #self.assertEqual(returned, expected)


    def test_requestStatusFromServer(self):
        """
        test_requestStatusFromServerrequestStatusFromServer:
        mock request from the server.
        TODO
        """
        mock = Mock()
        mock.tls.requestStatusFromServer()


    def test_writeAndSaveData(self):
        """
        test_writeAndSaveData:
        TODO
        """
        mock = Mock()
        mock.tls.writeAndSaveData()


    def test_createStatusURL(self):
        """
        test_createStatusURL:
        TODO
        """
        mock = Mock()
        mock.tls.createStatusURL()


    def test_returnValidModesString(self):
        """
        test_returnValidModesString:
        TODO
        """
        mock = Mock()
        mock.tls.returnValidModesString()


    def test_returnValidAllModesString(self):
        """
        test_returnValidAllModesString:
        TODO
        """
        mock = Mock()
        mock.tls.returnValidAllModesString()


if __name__=='__main__':
    unittest.main()
