#! /usr/bin/env python 

import unittest
from unittest.mock import Mock, patch
import src
from src import trainsLinesStatus as tls
from colorama import Fore
import datetime
import sys
import requests

class Testing(unittest.TestCase):
    """
    Testing: class that calls the functions
    of the program trainsLinesStatus.py
    """


    def test_configure_logger(self):
        """
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
                return_value = True)
    def test_check_last_time_executed_requests(self, return_value):
        """
        test_check_last_time_executed_requests:
        Test of the function determining whether
        a new request is necessary.
        """
        returned = tls.check_last_time_executed_requests()
        self.assertEqual(returned, True)


        ### OR ###


    def test_check_last_time_executed_requests_2(self):
        """
        test_check_last_time_executed_requests:
        Test of the function determining whether
        a new request is necessary.
        """
        patcher = patch('src.trainsLinesStatus.'
                'check_last_time_executed_requests', 
                return_value = False)
        patcher.start()
        returned = tls.check_last_time_executed_requests()
        self.assertEqual(returned, False)


    def test_check_last_time_executed_requests_exceptions(self):
        """
        test_check_last_time_executed_requests_exceptions:
        Test the exception raise of the function determining 
        whether a new request is necessary.
        """
        patcher = patch('src.trainsLinesStatus.'
                'check_last_time_executed_requests', 
                side_effect = Exception)
        patcher.start()
        with self.assertRaises(Exception):
            tls.check_last_time_executed_requests()


        ### OR ###


    def test_check_last_time_executed_requests_exceptions_2(self):
        """
        test_check_last_time_executed_requests_exceptions:
        Test the exception raise of the function determining 
        whether a new request is necessary.
        """
        open = Mock()
        tls.check_last_time_executed_requests.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            tls.check_last_time_executed_requests()


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


    #def test_print_saved_data(self): 
    #    """
    #    test_print_saved_data:
    #    Test of the function responsible
    #    for printing entries of a file
    #    to the terminal.
    #    """


    def test_request_status_from_server(self):
        """
        test_request_status_from_server:
        Test whether a request is performed, 
        and data are received. 
        """
        requests.get = Mock()
        with self.assertRaises(SystemExit):
            tls.request_status_from_server('a_url')


    def test_get_dictionary_key(self):
        """
        """
        example_dict = {'key_1' : 'val_1'}
        returned = tls.get_dictionary_key(example_dict, 'key_1')
        expected = example_dict.get('key_1')
        self.assertEqual(returned, expected)

        returned = tls.get_dictionary_key(example_dict, 'key_3')
        expected = None
        self.assertEqual(returned, expected)
            


    def test_write_save_data(self):
        """
        test_write_save_data:
        Tests whether a file opens, and the
        requested data are written as comma
        separated values.
        """
        correct_data = [
                {'name': 'a_name', 
                'lineStatuses': [
                    {'statusSeverity': '0',
                    'statusSeverityDescription': 'ok'}]
                }]
        tls.write_save_data(correct_data)
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
        sample = 'tube,tram'
        returned = tls.return_valid_modes_string(sample)
        self.assertEqual(sample, returned)

        sample = 'tram,tube'
        returned = tls.return_valid_modes_string(sample)
        expected = 'tube,tram'
        self.assertEqual(expected, returned)


    def test_return_all_valid_modes_string(self):
        """
        test_return_all_valid_modes_string:
        """


    def test_set_logger(self):
        """
        """


    def test_ttl_toRequest(self):
        """
        """


    def test_execute_request(self):
        """
        """


if __name__=='__main__':
    unittest.main()
