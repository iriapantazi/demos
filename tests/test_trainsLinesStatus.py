#! /usr/bin/env python 

import unittest
from unittest.mock import Mock, patch
import src
from src import trainsLinesStatus as tls
#import src.trainsLinesStatus as tls
from colorama import Fore
import datetime
import sys

class Testing(unittest.TestCase):
    """
    Testing: class that calls the functions
    of the program trainsLinesStatus.py
    """

    def test_detect_python_version(self):
        """
        test_detect_python_version:
        Test if python version is supported.
        """
        tls.detect_python_version()

        patcher = patch('sys.version_info', major=2, minor=7)
        patcher.start()
        with self.assertRaises(Exception): 
            tls.detect_python_version()


    @patch('src.trainsLinesStatus.'
                'check_last_time_executed_requests', 
                return_value = False)
    def test_check_last_time_executed_requests(self, return_value):
        """
        test_check_last_time_executed_requests:
        Test of the function determining whether
        a new request is necessary.
        """
        returned = tls.check_last_time_executed_requests()
        self.assertEqual(returned, False)


    def test_check_last_time_executed_requests(self):
        """
        test_check_last_time_executed_requests:
        Test of the function determining whether
        a new request is necessary.
        """
        patcher = patch('src.trainsLinesStatus.'
                'check_last_time_executed_requests', 
                return_value = True)
        patcher.start()
        returned = tls.check_last_time_executed_requests()
        self.assertEqual(returned, True)


    def test_associate_status_color(self):
        """
        test_associate_status_color:
        Test of the function assigning
        a color to a line status code.
        """
        colors = ['BLUE', 'CYAN', 'RED', 
                'MAGENTA', 'GREEN', 'YELLOW']
        colors = [getattr(Fore, i) for i in colors]
        for i in range(0, 100):
            returned = tls.associate_status_color(i)
            expected = colors[i % 6]
            self.assertEqual(returned, expected)


    def test_print_saved_data(self): 
        """
        test_print_saved_data:
        Test of the function responsible
        for printing entries of a file
        to the terminal.
        """
        returned = tls.print_saved_data()
        mock = Mock()
        print = mock


    def test_request_status_from_server(self):
        """
        test_request_status_from_server:
        Tests whether a request is performed, 
        and data are received. 
        """
        with patch('src.trainsLinesStatus.'
                'request_status_from_server') as mock_get:
            expected =  '' 
            mock_get.return_value.data = expected
            returned = tls.request_status_from_server('')
        #self.assertEqual(expected, returned)


    def test_write_save_data(self):
        """
        test_write_save_data:
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
        tls.write_save_data(sample_data)
        #self.assertEqual()


    def test_create_status_URL(self):
        """
        test_create_status_URL:
        Tests whether the appropriate url
        is created, and returns it.
        """
        returned = tls.create_status_URL('k')
        expected = f'{tls.TFLAPI}/line/mode/k/status'
        self.assertEqual(returned, expected)


    def test_return_valid_modes_string(self):
        """
        test_return_valid_modes_string:
        Tests whether the arguments parsed 
        are valid.
        """


    def test_return_all_valid_modes_string(self):
        """
        test_return_all_valid_modes_string:
        """


if __name__=='__main__':
    unittest.main()
